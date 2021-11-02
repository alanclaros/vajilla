"""database fields validators (numbers, strings, emails)"""
from decimal import Decimal
# import time
import re

dictionary_string = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'ñ', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                     'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'Ñ', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                     'á', 'é', 'í', 'ó', 'ú',
                     'Á', 'É', 'Í', 'Ó', 'Ú',
                     '"', "'", '@', '#', '%', '&', '/', '(', ')', '=', '?', '¿', '|', '!', '¡', '+', '*', '[', ']', '{', '}',
                     '<', '>', ',', ';', '.', ':', '-', '_', ' ',
                     '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


def validate_number_int(field_name, field_value, negatives='no', len_zero='no', min_value=None, max_value=None, custom_error_min='', custom_error_max=''):
    """
    convert object to int number
    :param field_name: (str) variable name
    :param field_value: (object) variable value
    :param negatives: (str) accept negatives or not
    :param min_value: (int) min value
    :param max_value: (int)  max value
    :param custom_error_min: (str) message error if value is lower min value
    :param custom_error_max: (str) message error if value is bigger max value
    :return: (int) int value
    """

    if not isinstance(field_name, str):
        raise AttributeError('Debe introducir el nombre de la variable')
    if field_name.strip() == '':
        raise AttributeError('Debe introducir un nombre valido para la variable')

    # tratamos de convertir el numero a entero
    try:
        field_str = str(field_value).strip()
        if len_zero == 'no':
            if field_str == '':
                raise ValueError('Debe ingresar un numero valido para ' + field_name)

            number = int(field_str)
        else:
            if field_str == '':
                number = 0
            else:
                number = int(field_str)

        # verificamos si puede ingresar negativos
        if negatives == 'no':
            if number < 0:
                raise ValueError('Debe ingresar un numero positivo para ' + field_name)

        # minimo valor
        if min_value:
            if number < min_value:
                if custom_error_min != '':
                    raise ValueError(custom_error_min + ' ' + str(min_value))
                else:
                    raise ValueError('El numero ' + field_name + ' no puede ser menor a ' + str(min_value))

        # maximo valor
        if max_value:
            if number > max_value:
                if custom_error_max != '':
                    raise ValueError(custom_error_max + ' ' + str(max_value))
                else:
                    raise ValueError('El numero ' + field_name + ' no puede ser mayor a ' + str(max_value))

        return number

    except Exception as ex:
        raise ValueError('Error al convertir la variable ' + field_name + ' a entero: ' + str(ex))


def validate_number_decimal(field_name, field_value, negatives='no', len_zero='no', min_value=None, max_value=None,
                            custom_error_min='',
                            custom_error_max=''):
    """
    convert object to decimal number
    :param field_name: (str) variable name
    :param field_value: (object) variable value
    :param negatives: (str) accept negatives or not
    :param min_value: (int) min value
    :param max_value: (int)  max value
    :param custom_error_min: (str) message error if value is lower min value
    :param custom_error_max: (str) message error if value is bigger max value
    :return: (Decimal) decimal value
    """

    if not isinstance(field_name, str):
        raise AttributeError('Debe introducir el nombre de la variable')
    if field_name.strip() == '':
        raise AttributeError('Debe introducir un nombre valido para la variable')

    # tratamos de convertir el numero a decimal
    try:
        field_str = str(field_value).strip()
        if len_zero == 'no':
            if field_str == '':
                raise ValueError('Debe ingresar un numero valido para ' + field_name)

            number = Decimal(field_str)
        else:
            if field_str == '':
                number = 0
            else:
                number = Decimal(field_str)

        # verificamos si puede ingresar negativos
        if negatives == 'no':
            if number < 0:
                raise ValueError('Debe ingresar un numero positivo para ' + field_name)

        # minimo valor
        if min_value:
            if number < min_value:
                if custom_error_min != '':
                    raise ValueError(custom_error_min + ' ' + str(min_value))
                else:
                    raise ValueError('El numero ' + field_name + ' no puede ser menor a ' + str(min_value))

        # maximo valor
        if max_value:
            if number > max_value:
                if custom_error_max != '':
                    raise ValueError(custom_error_max + ' ' + str(max_value))
                else:
                    raise ValueError('El numero ' + field_name + ' no puede ser mayor a ' + str(max_value))

        return number

    except Exception as ex:
        raise ValueError('Error al convertir la variable ' + field_name + ' a decimal: ' + str(ex))


def validate_string(field_name, field_value, remove_specials='no', len_zero='no'):
    """
    validate string to database, remove or not special characters
    :param field_name: (str) field name
    :param field_value: (str) field value
    :param remove_specials: (str) 'no' by default
    :param len_zero: (str) 'no' by default, dont remove special characters
    :return: (str) string value
    """

    # field name
    if not isinstance(field_name, str):
        raise AttributeError('Debe introducir el nombre de la variable')
    if field_name.strip() == '':
        raise AttributeError('Debe introducir un nombre valido para la variable')

    # tratamos de convertir a cadena
    try:
        cadena = str(field_value).strip()

        # tamanio de la cadena
        if len_zero == 'no':
            if cadena == '':
                raise ValueError('No puede ingresar una cadena vacia para ' + field_name)

        # remover caracteres especiales
        if remove_specials != 'no':
            nueva_cadena = ''
            for i in range(0, len(cadena)):
                if cadena[i:i + 1] in dictionary_string:
                    nueva_cadena += cadena[i:i + 1]

            if len_zero == 'no' and nueva_cadena == '':
                raise ValueError('los caracteres de ' + field_name + ' no estan en las letras permitidas')
        else:
            nueva_cadena = cadena

        return nueva_cadena

    except Exception as ex:
        raise ValueError('Error al convertir la variable a cadena: ' + str(ex))


def validate_email(field_name, email_value, len_zero='no'):
    """
    validate email address
    :param field_name: (str) variable name
    :param email_value: (str) email value
    :return: (str): email
    """
    correo = validate_string(field_name, email_value, remove_specials='yes', len_zero=len_zero)

    if len_zero == 'no':
        if correo == '':
            raise ValueError('Debe ingresar un email para ' + field_name)

        try:
            expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
            if re.match(expresion_regular, correo):
                return correo
            else:
                raise ValueError('Debe introducir un email valido para ' + field_name + ' (' + email_value + ')')

        except Exception as ex:
            raise ValueError('Error al validar el email ' + str(ex))
    else:
        if correo == '':
            return correo
        else:
            expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
            if re.match(expresion_regular, correo):
                return correo
            else:
                raise ValueError('Debe introducir un email valido para ' + field_name + ' (' + email_value + ')')
