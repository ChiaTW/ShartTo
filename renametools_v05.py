import maya.cmds as cmds
import re

# === UI Field Identifiers ===
SEARCH_FIELD = "searchField"
REPLACE_FIELD = "replaceField"
RENAME_FIELD = "renameField"
START_FIELD = "startField"
PADDING_FIELD = "paddingField"

def search_and_replace(*args):
    """ 在選取的物體名稱中搜尋並取代名稱 """
    search_text = cmds.textField(SEARCH_FIELD, query=True, text=True)
    replace_text = cmds.textField(REPLACE_FIELD, query=True, text=True)
    selected_objects = cmds.ls(selection=True)

    if not selected_objects:
        cmds.warning("Please select the object")
        return

    if not search_text:
        cmds.warning("Please enter a search text")
        return

    count = 0
    for obj in selected_objects:
        if search_text in obj:
            new_name = obj.replace(search_text, replace_text)
            cmds.rename(obj, new_name)
            count += 1


def rename_and_number(*args):
    """ 批次重命名並增加編號 """
    base_name = cmds.textField(RENAME_FIELD, query=True, text=True)
    start_number = cmds.intField(START_FIELD, query=True, value=True)
    padding = cmds.intField(PADDING_FIELD, query=True, value=True)
    selected_objects = cmds.ls(selection=True)

    if not selected_objects:
        cmds.warning("Please select the object")
        return

    if not base_name:
        cmds.warning("Please enter a new name")
        return

    # 禁止 base_name 為純數字
    if base_name.isdigit():
        base_name = '_' + base_name

    # 過濾不合法字符：只保留字母、數字、下劃線
    base_name = re.sub(r'[^a-zA-Z0-9_]', '', base_name)

    # 確保名稱不以數字開頭
    if base_name and base_name[0].isdigit():
        base_name = '_' + base_name

    count = 0
    for i, obj in enumerate(selected_objects,start=start_number):
        new_name = f"{base_name}_{str(i).zfill(padding)}"
        if cmds.objExists(new_name):
            cmds.warning(f"Object name '{new_name}' already exists!")
        else:
            cmds.rename(obj, new_name)
            count += 1


def rename_tool_ui():
    """ 建立 UI """
    if cmds.window("RenameTool", exists=True):
        cmds.deleteUI("RenameTool")

    window = cmds.window("RenameTool", title="Rename Tool_v04", widthHeight=(300, 200), sizeable=False)
    cmds.columnLayout(adjustableColumn=True)

    # 搜尋替換區塊
    cmds.separator(height=10, style="in")

    cmds.rowLayout(numberOfColumns=2, adjustableColumn=2)
    cmds.text(label="Search: ", align="right", width=50)
    cmds.textField(SEARCH_FIELD)
    cmds.setParent("..")

    cmds.separator(height=5, style="none")

    cmds.rowLayout(numberOfColumns=2, adjustableColumn=2)
    cmds.text(label="Replace: ", align="right", width=50)
    cmds.textField(REPLACE_FIELD)
    cmds.setParent("..")

    cmds.separator(height=5, style="none")
    cmds.button(label="Search and Replace", command=search_and_replace)

    # 分隔線
    cmds.separator(height=10, style="in")

    # 重命名與編號區塊
    cmds.rowLayout(numberOfColumns=2, adjustableColumn=2)
    cmds.text(label="New Name: ", align="right", width=70)
    cmds.textField(RENAME_FIELD)
    cmds.setParent("..")

    cmds.rowLayout(numberOfColumns=2)
    cmds.text(label="Start #: ", align="right", width=70)
    cmds.intField(START_FIELD, value=1, width=50, enterCommand=rename_and_number)
    cmds.setParent("..")

    cmds.rowLayout(numberOfColumns=2)
    cmds.text(label="Padding: ", align="right", width=70)
    cmds.intField(PADDING_FIELD, value=3, width=50, enterCommand=rename_and_number) 
    cmds.setParent("..")

    cmds.separator(height=5, style="none")
    cmds.button(label="Rename and Number", command=rename_and_number)

    cmds.separator(height=10, style="in")
    cmds.showWindow(window)

# 啟動 UI
rename_tool_ui()
