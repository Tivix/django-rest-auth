from django.utils.crypto import get_random_string


HASH_CHARACTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def generate_new_hash_with_length(length):
    """
    Generates a random string with the alphanumerical character set and given length.
    """
    return get_random_string(length, HASH_CHARACTERS)


# Based on http://stackoverflow.com/a/547867. Thanks! Credit goes to you!
def construct_modules_and_import(name):
    """
    Grab the Python string to import
    """

    # Get all the components by dot notations
    components = name.split('.')
    module = ''
    i = 1

    # Construct the partial Python string except the last package name
    for comp in components:
        if i < len(components):
            module += str(comp)

        if i < (len(components) - 1):
            module += '.'

        i += 1

    # Import the module from above python string
    mod = __import__(module)

    # Import the component recursivcely
    for comp in components[1:]:
        mod = getattr(mod, comp)

    # Return the imported module's class
    return mod
