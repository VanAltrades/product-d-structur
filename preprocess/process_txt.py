def get_dict_from_txt(txt_file='amazon-product-data.txt'):
    """
    Returns "d" dictionary extracted from txt file.
    Returns "unique_keys" set of unique key names -- needed for BQ table schema format.
    """
    # create an unstructured dictionary of the text file

    # Initialize an empty dictionary
    d = {}
    current_item = None  # Variable to keep track of the current item being processed

    # Initialize a set to store unique keys (used to make table schema)
    unique_keys = set()

    # Read the file
    with open(txt_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()  # Remove leading/trailing whitespace
            

            # Skip empty lines
            if not line:
                continue

            if line.startswith("ITEM"):
                # If a new item is encountered, create a new dictionary for it
                item_number = line.split()[1]
                d[item_number] = {}
                current_item = item_number
            # elif current_item:
            elif "=" in line:
                # If in a current item's block, split line into key and value
                split_line = line.split('=')
                if len(split_line) == 2:
                    key, value = split_line
                    d[current_item][key] = value

                    # Add the key to the unique set
                    unique_keys.add(key)
            else:
                continue
    return d, unique_keys


def get_structured_dict(d, unique_keys):
    """
    Returns "d_schema" dictionary with common schema format from unique_keys set.
    """
    # now loop through the d[current_item][key] records and add them to a unique set

    # Initialize the d_schema dictionary
    d_schema = {}

    # Loop through each item in d
    for item_key, item_data in d.items():
        d_schema[item_key] = {}  # Initialize the record in d_schema
        
        # Loop through unique keys
        for key in unique_keys:
            # Add the value if the key exists in the item_data
            if key in item_data:
                d_schema[item_key][key] = item_data[key]
            else:
                d_schema[item_key][key] = None  # Set None for missing keys
    return d_schema