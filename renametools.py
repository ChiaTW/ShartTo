import maya.cmds as cmds

def search_and_replace(*args):
    """ 在選取的物體名稱中搜尋並取代名稱 """
    search_text = cmds.textField("searchField", query=True, text=True)
    replace_text = cmds.textField("replaceField", query=True, text=True)
    selected_objects = cmds.ls(selection=True)

    if not selected_objects:
        cmds.warning("Please select the object")
        return

    if not search_text:
        cmds.warning("Please enter a new name")
        return

    for obj in selected_objects:
        if search_text in obj:
            new_name = obj.replace(search_text, replace_text)
            cmds.rename(obj, new_name)

    #cmds.inViewMessage(amg=f"已替换 {len(selected_objects)} 个物件的名称", pos="topCenter", fade=True)

def rename_and_number(*args):
    """批示重命名並增加編號 """
    base_name = cmds.textField("renameField", query=True, text=True)
    start_number = cmds.textField("startField", query=True, text=True)
    padding = cmds.textField("paddingField", query=True, text=True)
    selected_objects = cmds.ls(selection=True)

    if not selected_objects:
        cmds.warning("Please select the object")
        return

    if not base_name:
        cmds.warning("Please enter a new name")
        return

    # 新增：禁止 base_name 為純數字
    if base_name.isdigit():
        cmds.warning("The base name cannot be only numbers. Please use letters.")
        return

    # 過濾不合法字符：只保留字母、數字、下劃線
    base_name = re.sub(r'[^a-zA-Z0-9_]', '', base_name)

    # 確保名稱不以數字開頭
    if base_name[0].isdigit():
        base_name = '_' + base_name  # 加上一個合法的開頭字符

    try:
        start_number = int(start_number)
        padding = int(padding)
    except ValueError:
        cmds.warning("Start number and padding must be numbers!")
        return

    for i, obj in enumerate(selected_objects):
        # 組合新的物件名稱
        new_name = f"{base_name}_{str(start_number + i).zfill(padding)}"
        
        # 檢查名稱是否合法，如果非法則跳過
        if cmds.objExists(new_name):
            cmds.warning(f"Object name '{new_name}' already exists!")
        else:
            cmds.rename(obj, new_name)

    #cmds.inViewMessage(amg=f"已重命名 {len(selected_objects)} 个物件", pos="topCenter", fade=True)
def rename_tool_ui():
    ###  UI 界面 ###

    if cmds.window("RenameTool", exists=True):
        cmds.deleteUI("RenameTool")

    window = cmds.window("RenameTool", title="RenameTool", widthHeight=(300, 200), sizeable=False)

    cmds.columnLayout(adjustableColumn=True)

    # 搜尋替换 UI
    cmds.separator(height=10, style="in")
    cmds.rowLayout(numberOfColumns=2, adjustableColumn=2)
    cmds.text(label="Search: ", align="right", width=50)
    cmds.textField("searchField")
    cmds.setParent("..") 

    cmds.separator(height=5, style="none")

    cmds.rowLayout(numberOfColumns=2, adjustableColumn=2)
    cmds.text(label="Replace: ", align="right", width=50)
    cmds.textField("replaceField")
    cmds.setParent("..")

    cmds.separator(height=5, style="none")
    
    cmds.button(label="Search and Replace", command=search_and_replace)

    cmds.separator(height=10, style="in")

    # 重新命名並編號 UI
    cmds.rowLayout(numberOfColumns=2, adjustableColumn=2)
    cmds.text(label="Newname: ", align="right", width=70)
    cmds.textField("renameField")
    cmds.setParent("..")

    cmds.rowLayout(numberOfColumns=2)
    cmds.text(label="Start #: ", align="right", width=70)
    cmds.textField("startField", text="1", width=50)
    cmds.setParent("..")

    cmds.rowLayout(numberOfColumns=2)
    cmds.text(label="Padding: ", align="right", width=70)
    cmds.textField("paddingField", text="3", width=50)
    cmds.setParent("..")

    cmds.separator(height=5, style="none")
    
    cmds.button(label="Rename And Number", command=rename_and_number)
    
    cmds.separator(height=10, style="in")    

    cmds.showWindow(window)

rename_tool_ui()
