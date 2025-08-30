import json

if __name__ == "__main__":
    user_info = '[{"name":"郑秋实","id":"330127"}]'  # Corrected JSON: double quotes within the string
    try:
        user_info_dict = json.loads(user_info)
        print(user_info_dict)
        print(f"Hello, 参数 {user_info_dict}!")
    except json.JSONDecodeError:
        print(f"Invalid JSON: {user_info}")
        print(f"Hello, 无效的 JSON 参数: {user_info}!")
    except TypeError as e:
        print(f"Error processing JSON: {user_info}")
        print(f"Hello, 处理 JSON 参数时出错: {e}!")