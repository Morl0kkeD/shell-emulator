import xml.etree.ElementTree as ET
import os
import base64

class VFSNode:
    def __init__(self, name, is_dir=False, content="", owner="root"):
        self.name = name
        self.is_dir = is_dir
        self.content = content
        self.owner = owner
        self.children = {}  # name -> VFSNode

class VFS:
    def __init__(self):
        self.root = VFSNode("/", is_dir=True)
        self.current = self.root
        self.current_path = "/"
        self.name = "default"

    def load_from_xml(self, path: str) -> bool:
        if not os.path.exists(path):
            print(f"Ошибка: файл VFS не найден: {path}")
            return False

        try:
            tree = ET.parse(path)
            root_elem = tree.getroot()
            self.name = root_elem.get("name", "unnamed")

            self.root = VFSNode("/", is_dir=True)
            self.current = self.root
            self.current_path = "/"

            dir_elem = root_elem.find("directory")
            if dir_elem is not None:
                self._parse_directory(dir_elem, self.root)

            return True
        except Exception as e:
            print(f"Ошибка загрузки VFS: {e}")
            return False

    def _parse_directory(self, elem, node: VFSNode):
        for child in elem:
            name = child.get("name")
            owner = child.get("owner", "root")

            if child.tag == "directory":
                new_node = VFSNode(name, is_dir=True, owner=owner)
                node.children[name] = new_node
                self._parse_directory(child, new_node)
            elif child.tag == "file":
                content = child.get("content", "")
                encoding = child.get("encoding", "")
                if encoding == "base64":
                    try:
                        content = base64.b64decode(content).decode("utf-8", errors="replace")
                    except Exception:
                        content = "[binary data]"
                new_node = VFSNode(name, is_dir=False, content=content, owner=owner)
                node.children[name] = new_node

    def resolve_path(self, path: str):
        if not path or path == ".":
            return self.current

        if path.startswith("/"):
            node = self.root
            parts = [p for p in path.strip("/").split("/") if p]
        else:
            node = self.current
            parts = [p for p in path.split("/") if p]

        for part in parts:
            if part == ".":
                continue
            if part == "..":
                node = self.root
                continue
            if part not in node.children:
                return None
            node = node.children[part]

        return node

    def list_dir(self, path: str = "") -> str:
        node = self.resolve_path(path) if path else self.current
        if node is None:
            return f"Ошибка: путь не найден: {path}"
        if not node.is_dir:
            return f"Ошибка: это не директория: {path}"

        if not node.children:
            return "(пустая директория)"

        lines = []
        for name, child in sorted(node.children.items()):
            prefix = "d" if child.is_dir else "-"
            lines.append(f"{prefix}  {child.owner:10}  {name}")
        return "\n".join(lines)

    def change_dir(self, path: str) -> str:
        if not path:
            return "Ошибка: не указан путь"

        node = self.resolve_path(path)
        if node is None:
            return f"Ошибка: путь не найден: {path}"
        if not node.is_dir:
            return f"Ошибка: это не директория: {path}"

        self.current = node
        if path.startswith("/"):
            self.current_path = path.rstrip("/") or "/"
        else:
            self.current_path = (self.current_path.rstrip("/") + "/" + path).replace("//", "/")

        return f"Текущая директория: {self.current_path}"