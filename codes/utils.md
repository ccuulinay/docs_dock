1. To get difference between two JSON strings
```py
def get_changes_between_2_json_strings(json_str1, json_str2):
    
    from deepdiff import DeepDiff

    def _convert_path_to_jsonpath(dp_path_str):
        parsed_elements = deepdiff.parse_path(dp_path_str)
        json_path_parts = ["$"]
        for element in parsed_elements:
            if isinstance(element, int):
                json_path_parts.append(f"[{element}]")
            else:
                json_path_parts.append(f".{element}")
        formatted_json_path = "".join(json_path_parts).replace(".$", "$")
        if formatted_json_path.startswith("$.["):
            formatted_json_path = formatted_json_path.replace("$.[", "$[", 1)

        return formatted_json_path

    if json_str1 and json_str2:
        try:
            # Parse JSON strings
            obj1 = json.loads(json_str1)
            obj2 = json.loads(json_str2)

            # Generate diff using DeepDiff
            ddiff = DeepDiff(
                obj1, obj2, 
                # view='text', 
            verbose_level=2)

            if ddiff:
                changes = []
                if 'values_changed' in ddiff:
                    for path, values in ddiff['values_changed'].items():
                        jpath = _convert_path_to_jsonpath(path)
                        changes.append({
                            "type": "update",
                            "jsonpath": jpath,
                            "path": path,
                            "old_value": values['old_value'],
                            "new_value": values['new_value']
                        })
                if 'dictionary_item_added' in ddiff:
                    for path in ddiff['dictionary_item_added']:
                        jpath = _convert_path_to_jsonpath(path)
                        changes.append({
                            "type": "add",
                            "jsonpath": jpath,
                            "path": path,
                            "value": "Value not directly available in diff"
                        })
                if 'dictionary_item_removed' in ddiff:
                    for path in ddiff['dictionary_item_removed']:
                        jpath = _convert_path_to_jsonpath(path)
                        changes.append({
                            "type": "delete",
                            "jsonpath": jpath,
                            "path": path,
                            "value": "Value not directly available in diff"
                        })
                if 'iterable_item_added' in ddiff:
                    for path, value in ddiff['iterable_item_added'].items():
                        jpath = _convert_path_to_jsonpath(path)
                        changes.append({
                            "type": "add",
                            "jsonpath": jpath,
                            "path": path,
                            "value": value
                        })
                if 'iterable_item_removed' in ddiff:
                    for path, value in ddiff['iterable_item_removed'].items():
                        jpath = _convert_path_to_jsonpath(path)
                        changes.append({
                            "type": "delete",
                            "jsonpath": jpath,
                            "path": path,
                            "value": value
                        })
                return changes
            else:
                logging.warning(f"Two JSON objects are identical.")

            
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON provided: {e}")
            logging.exception(e)
            
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            logging.exception(e)
    else:
        logging.warning("Please provide both JSON inputs.")
```
