'''
Module for customized message about the task results.
'''

def message(name, test_result)->str:
    '''
    This function creates the customized message about test results
    '''
    intro = f" { name } done!  "
    result = f"Result: {test_result}"

    length = len(intro)/2
    # length_between_stars =
    if length % 2 != 0:
        print(length)
        length = round(length)
        intro += " "
    length = int(length)

    message = f"""
{'* '*(length)}*\n*{'  '*(length)}*
*{intro}*
*{' '*(length-7)}{result}{' '*(length-7)}*
*{'  '*(length)}*\n{'* '*(length)}*\n
    """
    return message