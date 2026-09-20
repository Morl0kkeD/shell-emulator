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

    def get_size(self) -> int:
        if not self.is_dir:
            return len(self.content.encode('utf-8'))
        return sum(child.get_size() for child in self.children.values())

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
            return f"ls: невозможно получить доступ к '{path}': Нет такого файла или каталога"
        if not node.is_dir:
            return f"d  {node.owner:10}  {node.name}"

        if not node.children:
            return "(пустая директория)"

        lines = []
        for name, child in sorted(node.children.items()):
            prefix = "d" if child.is_dir else "-"
            lines.append(f"{prefix}  {child.owner:10}  {name}")
        return "\n".join(lines)

    def change_dir(self, path: str) -> str:
        if not path:
            return "cd: не указан путь"

        node = self.resolve_path(path)
        if node is None:
            return f"cd: {path}: Нет такого файла или каталога"
        if not node.is_dir:
            return f"cd: {path}: Не является каталогом"

        self.current = node

        if path.startswith("/"):
            raw_path = path
        else:
            raw_path = self.current_path.rstrip("/") + "/" + path

        parts = []
        for p in raw_path.split("/"):
            if p == "" or p == ".":
                continue
            if p == "..":
                if parts:
                    parts.pop()
            else:
                parts.append(p)

        self.current_path = "/" + "/".join(parts)
        return f"Текущая директория: {self.current_path}"

    def du(self, path: str = "") -> str:
        target = self.resolve_path(path) if path else self.current
        if target is None:
            return f"du: невозможно получить доступ к '{path}': Нет такого файла или каталога"

        lines = []
        if target.is_dir:
            for name, child in target.children.items():
                lines.append(f"{child.get_size()}\t{name}")
            lines.append(f"{target.get_size()}\t.")
        else:
            lines.append(f"{target.get_size()}\t{target.name}")
        return "\n".join(lines)

    def wc(self, path: str) -> str:
        if not path:
            return "wc: не указан файл"

        node = self.resolve_path(path)
        if node is None:
            return f"wc: {path}: Нет такого файла или каталога"
        if node.is_dir:
            return f"wc: {path}: Это каталог"

        content = node.content
        lines_count = len(content.splitlines()) if content else 0
        words_count = len(content.split()) if content else 0
        bytes_count = len(content.encode('utf-8'))

        return f"  {lines_count}  {words_count} {bytes_count} {node.name}"

    def touch(self, filename: str) -> str:
        if not filename:
            return "touch: не указано имя файла"

        if "/" in filename:
            parent_path, name = filename.rsplit("/", 1)
            parent_node = self.resolve_path(parent_path if parent_path else "/")
        else:
            parent_node = self.current
            name = filename

        if parent_node is None or not parent_node.is_dir:
            return f"touch: невозможно создать файл '{filename}': Нет такого файла или каталога"

        if name in parent_node.children:
            return ""  # В UNIX touch для существующего файла просто обновляет время доступа

        parent_node.children[name] = VFSNode(name, is_dir=False, content="", owner="root")
        return ""

    def chown(self, new_owner: str, path: str) -> str:
        if not new_owner or not path:
            return "chown: не указаны параметры (использование: chown OWNER PATH)"

        node = self.resolve_path(path)
        if node is None:
            return f"chown: не удалось получить доступ к '{path}': Нет такого файла или каталога"

        node.owner = new_owner
        return ""