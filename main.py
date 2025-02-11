import os

import CrossDown
import markdown
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QSplitter,
    QTreeView, QTextEdit, QToolBar, QWidget, QVBoxLayout, QTextBrowser
)
from PyQt6.QtGui import QAction, QFileSystemModel
from PyQt6.QtCore import Qt, QDir


class MarkdownEditor(QMainWindow):
    def __init__(self):
        """
        初始化
        """
        super().__init__()
        self.editor = None
        self.preview = None
        self.model = None
        self.file_tree = None
        self.init_ui()
        self.setWindowTitle("PyUEE")
        self.resize(1200, 800)

    def init_ui(self):
        """
        UI初始化
        :return:
        """
        # 创建主分割器
        main_splitter = QSplitter()

        # 左侧文件树
        self.file_tree = QTreeView()
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.homePath())
        self.file_tree.setModel(self.model)
        self.file_tree.setRootIndex(self.model.index(QDir.homePath()))
        self.file_tree.doubleClicked.connect(self.open_file)

        # 中间编辑区域
        mid_widget = QWidget()
        mid_layout = QVBoxLayout(mid_widget)
        mid_layout.setContentsMargins(0, 0, 0, 0)

        # 工具栏
        toolbar = QToolBar()
        copy_action = QAction("📋 复制全文", self)
        copy_action.triggered.connect(self.copy_all)
        toolbar.addAction(copy_action)

        # 编辑器
        self.editor = QTextEdit()
        self.editor.textChanged.connect(self.update_preview)

        mid_layout.addWidget(toolbar)
        mid_layout.addWidget(self.editor)

        # 右侧预览区域
        self.preview = QTextBrowser()

        # 添加组件到主分割器
        main_splitter.addWidget(self.file_tree)
        main_splitter.addWidget(mid_widget)
        main_splitter.addWidget(self.preview)
        main_splitter.setSizes([200, 500, 500])

        self.setCentralWidget(main_splitter)

    def open_file(self, index):
        """
        打开文件
        :param index: 要显示在文件树的目录
        :return:
        """
        path = self.model.filePath(index)
        if os.path.isfile(path) and path.endswith('.md'):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    self.editor.setPlainText(f.read())
            except Exception as e:
                print(f"打开文件失败: {e}")

    def update_preview(self):
        html, meta = CrossDown.main(self.editor.toPlainText(), variable={})  # 解析markdown
        full_html = f"""<!DOCTYPE html>  
<html lang="zh-CN">  
<head>  
    <meta charset="UTF-8">  
    <meta name="viewport" content="width=device-width, initial-scale=1.0">  
    <title>UTF-8编码示例</title>  
{CrossDown.indent(list(CrossDown.HEAD.values()))}
</head>  
<body>
{CrossDown.indent(html, 4)}
</body>  
</html>
"""
        self.preview.setHtml(full_html)

    def copy_all(self):
        """
        复制工具
        :return:
        """
        text = self.editor.toPlainText()
        QApplication.clipboard().setText(text)


if __name__ == "__main__":
    app = QApplication([])
    window = MarkdownEditor()
    window.show()
    app.exec()
