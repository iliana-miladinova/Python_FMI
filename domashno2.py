def is_valid_value(val): 
    valid_bushes_values = ['храст', 'shrub', 'bush']
    if type(val) is dict: 
        if val.get('name'):
            if val['name'].lower() in valid_bushes_values:
                return True
    return False


def function_that_says_ni(*args, **kwargs):
    cost = 0
    unique_letters_in_name = set()
    
    for arg in args:
        if is_valid_value(arg):
            current_cost = arg.get('cost', 0)
            cost += current_cost
                    
    for key, val in kwargs.items():
        if is_valid_value(val):
            current_cost = val.get('cost', 0)
            cost += current_cost
            for letter in key:
                unique_letters_in_name.add(letter)

    if cost > 42: 
        return 'Ni!'
    
    whole_part_of_cost = int(cost)

    unique_letters_in_name_count = len(unique_letters_in_name)

    if whole_part_of_cost == 0 or unique_letters_in_name_count % whole_part_of_cost != 0:
        return 'Ni!'

    return f'{cost:.2f}лв'