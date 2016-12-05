def snake_to_camel(snake_case):
    split = snake_case.split('_')
    return ''.join([split[0]] + [x.title() for x in split[1:]])


def camel_to_snake(camel_case):
    camel_case = list(camel_case)
    capital_indices = [x for x, y in enumerate(camel_case) if y.isupper()]
    capital_indices.reverse()
    for index in capital_indices:
        if index == 0:
            continue
        camel_case.insert(index, '_')
    return ''.join(camel_case).lower()


def dict_transform(input_dict, func):
    output_dict = dict()

    for key, value in input_dict.items():
        if isinstance(value, dict):
            value = dict_transform(value, func)
        elif not isinstance(value, str) and hasattr(value, '__iter__'):  # Might be a list of dictionaries
            output_value = list()
            for element in value:
                if isinstance(value, dict):
                    output_value.append(dict_transform(element, func))
                else:
                    output_value.append(element)
            value = output_value

        output_dict[func(key)] = value

    return output_dict


def dict_to_snake(input_dict):
    return dict_transform(input_dict, camel_to_snake)


def dict_to_camel(input_dict):
    return dict_transform(input_dict, snake_to_camel)
