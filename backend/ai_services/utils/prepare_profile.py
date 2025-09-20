from typing import Dict, Union, List, Any, Set

default_excluded_keys = {'id', 'first_name', 'last_name', 'experience_years', 'experience_months', 'created_at', 'updated_at'}

def get_text_profile(user_profile: Dict[str, Any], excluded_keys: Union[Set[str], List[str]] = default_excluded_keys) -> str:
    lines = []    
    if excluded_keys is None:
        keys_to_process = user_profile.keys()
    else:
        excluded_keys_set = set(excluded_keys)
        keys_to_process = [key for key in user_profile.keys() if key not in excluded_keys_set]
    
    for key in keys_to_process:
        value = user_profile[key]
        if isinstance(value, (list, tuple, set)):
            formatted_value = ", ".join(str(item) for item in value)
            lines.append(f"{key}: {formatted_value}")
        else:
            lines.append(f"{key}: {value}")
    text_profile = "\n".join(lines)
    return text_profile