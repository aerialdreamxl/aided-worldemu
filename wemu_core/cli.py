import sys
import argparse
from pathlib import Path
from wemu_core.data.dataCore import newInstance, loadInstance, saveInstance

# 常量定义
VERSION = "Pre-Alpha"
DEFAULT_INSTANCE = {}
MENU_OPTIONS = {
    0: "Exit WEMU CLI",
    1: "WEMU instance operations", 
    2: "Show help",
    9: "Test Options"
}
INSTANCE_MENU_OPTIONS = {
    0: "Back",
    1: "Load",
    2: "New", 
    3: "Save",
    4: "Edit"
}

# 全局状态
instance = None

def get_user_input(prompt="> ", input_type=int, default=None):
    """安全获取用户输入，带类型转换和错误处理"""
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input and default is not None:
                return default
            if input_type == int:
                return int(user_input)
            elif input_type == str:
                return user_input
            else:
                return input_type(user_input)
        except ValueError:
            print(f"Invalid input. Expected {input_type.__name__}. Please try again.")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            return None
        except EOFError:
            print("\nInput ended unexpectedly.")
            return None

def format_status_line():
    """格式化状态行显示"""
    line = "="*50
    title = "WEMU - World Emulator"
    separator = "-"*50
    
    print(line)
    print(f"{title:^50}")
    print(line)
    
    if instance is None:
        print("Now Loaded: None")
    else:
        print(f"Now Loaded: {instance.get('name', 'Unknown')}")
    
    print(separator)

def display_menu(options_dict, title="Menu"):
    """统一的菜单显示函数"""
    print(f"\n{title}:")
    for key, value in options_dict.items():
        print(f"[{key}] {value}")

def instanceOps():
    """实例操作主循环"""
    while True:
        format_status_line()
        display_menu(INSTANCE_MENU_OPTIONS, "Instance Operations")
        
        inp = get_user_input()
        if inp is None:
            continue # 用户取消了操作
            
        if inp in INSTANCE_MENU_OPTIONS:
            if inp == 0:
                break  # 返回主菜单
            elif inp == 1:
                load_instance()
            elif inp == 2:
                new_instance()
            elif inp == 3:
                save_instance()
            elif inp == 4:
                edit_instance()
        else:
            print("Invalid option. Please select a valid option.")

def load_instance():
    """使用dataCore加载实例"""
    global instance
    instance_name = get_user_input("Enter instance name to load: ", input_type=str)
    if instance_name is None:
        return  # 用户取消操作
    if not instance_name.strip():
        print("Instance name cannot be empty!")
        return
    
    try:
        # 尝试从userdata目录加载实例
        instance_path = Path("userdata") / instance_name
        if not instance_path.exists():
            print(f"Instance '{instance_name}' does not exist!")
            return
            
        instance = loadInstance(instance_path)
        print(f"Instance '{instance_name}' loaded successfully!")
    except FileNotFoundError:
        print(f"Instance '{instance_name}' not found!")
    except Exception as e:
        print(f"Error loading instance: {str(e)}")

def new_instance():
    """使用dataCore创建新实例"""
    global instance
    instance_name = get_user_input("Enter new instance name: ", input_type=str)
    if instance_name is None:
        return  # 用户取消操作
    if not instance_name.strip():
        print("Instance name cannot be empty!")
        return
    
    # 创建新实例
    instance = newInstance(name=instance_name)
    print(f"New instance '{instance_name}' created successfully!")

def save_instance():
    """使用dataCore保存实例"""
    global instance
    if instance is None:
        print("No instance loaded to save!")
        return
    
    try:
        # 保存实例到userdata目录
        saveInstance(userDataPath=Path("userdata"), instance=instance)
        print(f"Instance '{instance.get('name')}' saved successfully!")
    except Exception as e:
        print(f"Error saving instance: {str(e)}")

def edit_instance():
    """编辑实例功能"""
    global instance
    if instance is None:
        print("No instance loaded to edit!")
        return
    
    print(f"Editing instance: {instance.get('name')}")
    
    while True:
        print(f"\nCurrent instance name: {instance.get('name')}")
        print("[0] Back")
        print("[1] Change name")
        print("[2] Edit configuration (placeholder)")
        inp = get_user_input()
        if inp is None:
            continue
        if inp == 0:
            break
        elif inp == 1:
            new_name = get_user_input(f"Enter new name for instance (current: '{instance.get('name')}'): ", input_type=str)
            if new_name is not None and new_name.strip():
                old_name = instance["name"]
                instance["name"] = new_name
                print(f"Instance renamed from '{old_name}' to '{new_name}' successfully!")
            elif new_name is not None:  # 空名称
                print("Instance name cannot be empty!")
        elif inp == 2:
            print("Configuration editing is not implemented yet.")
        else:
            print("Invalid option. Please select a valid option.")

def show_help():
    """显示详细帮助信息"""
    print("\n" + "="*60)
    print("WEMU CLI Help - World Emulator Command Line Interface")
    print("="*60)
    print("DESCRIPTION:")
    print("  WEMU is a World Emulator that allows you to simulate and manage")
    print("  various world environments and instances.")
    print("\nCOMMAND LINE OPTIONS:")
    print("  --version              Show version information")
    print("  --load INSTANCE_NAME   Load a specific instance at startup")
    print("  --new INSTANCE_NAME    Create a new instance at startup")
    print("  --non-interactive      Run in non-interactive mode")
    print("\nMAIN MENU OPTIONS:")
    print("  [0] Exit WEMU CLI      - Quit the program")
    print("  [1] Instance Ops       - Manage emulator instances (Load, New, Save, Edit)")
    print("  [2] Show Help          - Display this help message")
    print("  [9] Test Options       - Debug/test related features")
    print("\nINSTANCE OPERATIONS:")
    print("  [0] Back               - Return to main menu")
    print("  [1] Load               - Load an existing instance")
    print("  [2] New                - Create a new instance")
    print("  [3] Save               - Save the current instance")
    print("  [4] Edit               - Modify instance properties")
    print("\nFor more information, visit the project documentation.\n")
    print("="*60)

def test_options():
    """测试选项功能"""
    print("Test options functionality goes here...")
    print(f"WEMU Core Version: Unknown")  # wemu_core包未定义版本
    print(f"CLI Version: {VERSION}")

def main():
    global instance  # 将全局变量声明移到函数开头
    parser = argparse.ArgumentParser(description='WEMU - World Emulator CLI')
    parser.add_argument('--version', action='store_true', help='Show version information')
    parser.add_argument('--load', metavar='INSTANCE_NAME', help='Load a specific instance at startup')
    parser.add_argument('--new', metavar='INSTANCE_NAME', help='Create a new instance at startup')
    parser.add_argument('--non-interactive', action='store_true', help='Run in non-interactive mode')
    args = parser.parse_args()

    if args.version:
        print(f"WEMU CLI Version: {VERSION}")
        print(f"WEMU Core Version: Unknown")  # wemu_core包未定义版本
        return

    # 根据命令行参数执行相应操作
    if args.load:
        try:
            instance_path = Path("userdata") / args.load
            if instance_path.exists():
                instance = loadInstance(instance_path)
                print(f"Loaded instance '{args.load}' from command line.")
            else:
                print(f"Instance '{args.load}' does not exist! Creating new instance with that name.")
                instance = newInstance(name=args.load)
        except Exception as e:
            print(f"Error loading instance: {str(e)}")
            return
    
    if args.new:
        instance = newInstance(name=args.new)
        print(f"Created new instance '{args.new}' from command line.")
    
    if args.non_interactive:
        print("Non-interactive mode is not fully implemented yet.")
        # 在非交互模式下，可能只执行命令行参数指定的操作，然后退出
        if args.load or args.new:
            print("Operation completed in non-interactive mode.")
        return

    print("Welcome to WEMU CLI Version " + VERSION)
    while True:
        format_status_line()
        display_menu(MENU_OPTIONS, "Main Menu")
        inp = get_user_input()
        if inp is None:
            continue # 用户取消了操作
        if inp in MENU_OPTIONS:
            if inp == 0:
                break
            elif inp == 1:
                instanceOps()
            elif inp == 2:
                show_help()
            elif inp == 9:
                test_options()
        else:
            print("Invalid option. Please select a valid option.")

if __name__ == "__main__":
    main()