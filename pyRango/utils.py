def snake_to_camel(snake_case):
    split = snake_case.split('_')
    return ''.join([split[0]] + [x.title for x in split[1:]])


def dict_to_camel(input_dict):
    output_dict = dict()

    for key, value in input_dict.items():
        if isinstance(value, dict):
            value = dict_to_camel(value)
        elif hasattr(value, '__iter__'):  # Might be a list of dictionaries
            output_value = list()
            for element in value:
                if isinstance(value, dict):
                    output_value.append(dict_to_camel(element))
                else:
                    output_value.append(element)
            value = output_value

        output_dict[snake_to_camel(key)] = value

    return output_dict
