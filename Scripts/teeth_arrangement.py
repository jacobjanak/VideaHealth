"""
This script use the algorithm mentioned in https://www.nature.com/articles/s41598-019-40414-y
under "Application of teeth arrangement rules" section.

General algorithm:
    1) separating the boxes in an image to either be in upper teeth or lower teeth
by each box tooth label number.
    2) arranges each boxes in predictions upper & lower list by its x-value to match how it actually laid out in the image.
    3) slides the previous list against the teeth numbering system and compute which spot match the system the most.
    4) Once it found the best spot, it relabel all prediction boxes to be how the system order the teeth.

scoring system:
    in each sliding spot of the list, we compute the total score of this sliding spot.
    If a tooth is perfectly match the system (by its index & label number), its score is prediction score * 100.
    Else, its score is prediction score * 100 * the similarity ratio between prediction and the system tooth.

similarity ratio:
    similarity is computed by the prediction tooth category against the system tooth category.
    table 1 is used to convert teeth number to be its category
    table 2 is used to find the similarity ratio between (prediction tooth, system tooth)

Args:
    images ([Image]): a list of images containing input boxes

Returns:
    result_images ([Image]): a list of images containing output boxes that has been relabeled
"""

# Upper and Lower teeth numbering system
upper_teeth = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
lower_teeth = [32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17]

# table 1 Teeth categorization table: W=Wisdom, M=Molar, P=Premolar, Ca=Canine
#                                   , La=Lateral Incisor, Ce=Central Incisor, I=Incisor.
# OLD data structure for teeth category
# teeth_category = [(1, 'W'), (2, 'M'), (3, 'M'), (4, 'P'), (5, 'P'), (6, 'Ca'), (7, 'La'), (8, 'Ce'), (9, 'Ce'), (10, 'La'), (11, 'Ca'), (12, 'P'), (13, 'P'), (14, 'M'), (15, 'M'), (16, 'W')
#                   ,(32, 'W'), (31, 'M'), (30, 'M'), (29, 'P'), (28, 'P'), (27, 'Ca'), (26, 'I'), (25, 'I'), (24, 'I'), (23, 'I'), (22, 'Ca'), (21, 'P'), (20, 'P'), (19, 'M'), (18, 'M'), (17, 'W')]

teeth_category = {1:'W', 2:'M', 3:'M', 4:'P', 5:'P', 6:'Ca', 7:'La', 8:'Ce', 9:'Ce', 10:'La', 11:'Ca', 12:'P', 13:'P', 14:'M', 15:'M', 16:'W'
                  , 32:'W', 31:'M', 30:'M', 29:'P', 28:'P', 27:'Ca', 26:'I', 25:'I', 24:'I', 23:'I', 22:'Ca', 21:'P', 20:'P', 19:'M', 18:'M', 17:'W'}

# table 2 Similarity matrix between teeth categories for mismatches.
similarity_matrix = {'Upper': {('W', 'W'): 0.9, ('W', 'M'): 0.8, ('W', 'P'): 0., ('W', 'Ca'): 0., ('W', 'La'): 0., ('W', 'Ce'): 0.
                               ,('M', 'W'): 0.8, ('M', 'M'): 0.9, ('M', 'P'): 0., ('M', 'Ca'): 0., ('M', 'La'): 0., ('M', 'Ce'): 0.
                               ,('P', 'W'): 0., ('P', 'M'): 0., ('P', 'P'): 0.9, ('P', 'Ca'): 0.6, ('P', 'La'): 0.4, ('P', 'Ce'): 0.4
                               ,('Ca', 'W'): 0., ('Ca', 'M'): 0., ('Ca', 'P'): 0.6, ('Ca', 'Ca'): 0.9, ('Ca', 'La'): 0.6, ('Ca', 'Ce'): 0.8
                               ,('La', 'W'): 0., ('La', 'M'): 0., ('La', 'P'): 0.4, ('La', 'Ca'): 0.6, ('La', 'La'): 0.9, ('La', 'Ce'): 0.8
                               ,('Ce', 'W'): 0., ('Ce', 'M'): 0., ('Ce', 'P'): 0.4, ('Ce', 'Ca'): 0.8, ('Ce', 'La'): 0.8, ('Ce', 'Ce'): 0.9}
                    ,'Lower': {('W', 'W'): 0.9, ('W', 'M'): 0.7, ('W', 'P'): 0., ('W', 'Ca'): 0., ('W', 'I'): 0.
                               ,('M', 'W'): 0.7, ('M', 'M'): 0.9, ('M', 'P'): 0., ('M', 'Ca'): 0., ('M', 'I'): 0.
                               ,('P', 'W'): 0., ('P', 'M'): 0., ('P', 'P'): 0.9, ('P', 'Ca'): 0.5, ('P', 'I'): 0.3
                               ,('Ca', 'W'): 0., ('Ca', 'M'): 0., ('Ca', 'P'): 0.5, ('Ca', 'Ca'): 0.9, ('Ca', 'I'): 0.5
                               ,('I', 'W'): 0., ('I', 'M'): 0., ('I', 'P'): 0.3, ('I', 'Ca'): 0.5, ('I', 'I'): 0.9}}


def teeth_arrangements(images):
    imgs = []
    for image in images:
        imgs.append(teeth_arrangement(image))
    return imgs


def teeth_arrangement(image):
    upper_pred = []
    lower_pred = []
    upper_score = []
    lower_score = []

    # sort the boxes by x1 value
    image.outputBoxes = sorted(image.outputBoxes, key=lambda box: box.x1s)

    # separate upper and lower teeth in this image
    for box in image.outputBoxes:
        # get only the number of this tooth label
        label_num = int(box.label.strip('tooth_'))
        # Upper
        if label_num in upper_teeth:
            upper_pred.append(label_num)
            upper_score.append(box.score)
        # Lower
        elif label_num in lower_teeth:
            lower_pred.append(label_num)
            lower_score.append(box.score)
        # Error
        else:
            print('Error teeth arrangement: ' + str(label_num))

    # find section of upper teeth
    upper_i = max_comparison_score_index(upper_score, upper_pred, upper_teeth)

    # find section of lower teeth
    lower_i = max_comparison_score_index(lower_score, lower_pred, lower_teeth)

    # relabel the predictions
    for box in image.outputBoxes:
        # get only the number of this tooth label
        label_num = int(box.label.strip('tooth_'))
        # Upper
        if label_num in upper_teeth:
            box.label = 'tooth_' + str(upper_teeth[upper_i])
            upper_i += 1
        # Lower
        elif label_num in lower_teeth:
            box.label = 'tooth_' + str(lower_teeth[lower_i])
            lower_i += 1
        # Error
        else:
            print('Error teeth arrangement: ' + str(label_num))
    return image


def max_comparison_score_index(scores, pred, template):
    length = len(pred)
    max_index = -1
    max_score = -1

    # find index with max comparison score
    for i in range(len(template) - length + 1):
        score = comparison_score(scores, pred, template[i: i + length])
        if score > max_score:
            max_index = i
            max_score = score

    return max_index


# find a comparison score for a section of the template against the prediction
def comparison_score(scores, pred, sliced_template):
    score = 0
    for i, (p, t) in enumerate(zip(pred, sliced_template)):
        if p == t:  # same label => match score
            score += (scores[i] * 100)
        else:  # mismatch score
            score += (scores[i] * 100) * similarity(p, t)
    return score


# return the similarity ratio for tooth1 and tooth2.
# both teeth must be either in upper row or lower row
def similarity(tooth_num1, tooth_num2):
    # get the teeth number label
    # num1 = int(tooth1.label.strip('tooth_'))
    # num2 = int(tooth2.label.strip('tooth_'))

    # tooth category for the matrix
    cat1 = teeth_category[tooth_num1]
    cat2 = teeth_category[tooth_num2]

    # find if both teeth are in upper row or lower row
    dentition_section = ''
    if tooth_num1 in upper_teeth and tooth_num2 in upper_teeth:
        dentition_section = 'Upper'
    elif tooth_num1 in lower_teeth and tooth_num2 in lower_teeth:
        dentition_section = 'Lower'
    else:
        print('ERROR comparing upper tooth with lower tooth')

    return similarity_matrix[dentition_section][(cat1, cat2)]