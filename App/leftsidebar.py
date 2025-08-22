import flet as ft
from AgentUtils.clientInfo import clientInfo
from AgentUtils.ExpiringDictStorage import ExpiringDictStorage
from Business.translateConfig import TranslationContext


class LeftSidebar(ft.Container):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.visible = True
        self.storage = ExpiringDictStorage(expiry_days=7)

        # 创建输入字段的引用，以便在保存时获取值
        self.api_key_field = ft.TextField(
            password=True,
            can_reveal_password=True,
            value="",  # 默认值为空
        )

        self.base_url_field = ft.TextField(
            value="https://api.deepseek.com",  # 默认值
        )

        self.model_field = ft.TextField(
            value="deepseek-chat",  # 默认值
        )

        self.target_language_field = ft.TextField(
            value="zh",  # 默认值
        )

        self.reserved_word_field = ft.TextField(
            value="",  # 默认值为空
        )

        self.auto_detect_switch = ft.Switch(label="自动检测语言", value=True)
        self.pronunciation_switch = ft.Switch(label="发音功能", value=False)
        self.save_history_switch = ft.Switch(label="保存翻译历史", value=True)

        # 创建导航项目
        self.nav_items = [
            ft.NavigationRailDestination(
                label_content=ft.Text("Settings"),
                label="Settings",
                icon=ft.Icons.SETTINGS_OUTLINED,
                selected_icon=ft.Icons.SETTINGS,
            ),
            ft.NavigationRailDestination(
                label_content=ft.Text("历史"),
                label="历史",
                icon=ft.Icons.HISTORY_OUTLINED,
                selected_icon=ft.Icons.HISTORY,
            ),
        ]

        self.nav_rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            on_change=self.nav_change,
            destinations=self.nav_items,
            bgcolor=ft.Colors.BLUE_GREY_50,
            extended=True,
            height=110,
        )

        # 创建设置内容 - 使用可滚动容器
        self.settings_content = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Settings", style=ft.TextThemeStyle.HEADLINE_SMALL),
                    ft.Divider(),
                    # API Key 输入框
                    ft.Text("API Key:"),
                    self.api_key_field,
                    # Base URL 输入框
                    ft.Text("Base URL:"),
                    self.base_url_field,
                    # Model 输入框
                    ft.Text("Model:"),
                    self.model_field,
                    # Target Language 输入框
                    ft.Text("Target Language:"),
                    self.target_language_field,
                    # Reserved Word 输入框
                    ft.Text("Reserved Word:"),
                    self.reserved_word_field,
                    # 保留的开关选项
                    self.auto_detect_switch,
                    self.pronunciation_switch,
                    self.save_history_switch,
                    # 保存按钮固定在底部
                    ft.Container(
                        content=ft.ElevatedButton(
                            "保存设置",
                            icon=ft.Icons.SAVE,
                            on_click=self.save_settings,
                            width=200,
                        ),
                        alignment=ft.alignment.center,
                        padding=ft.padding.only(top=20),
                    ),
                ],
                spacing=15,
                scroll=ft.ScrollMode.AUTO,
            ),
            # 添加滚动和最大高度限制
            height=500,  # 限制最大高度
        )

        # 创建历史内容
        self.history_content = ft.Column(
            [
                ft.Text("翻译历史", style=ft.TextThemeStyle.HEADLINE_SMALL),
                ft.Divider(),
                ft.ListView(
                    controls=[
                        ft.ListTile(
                            title=ft.Text("你好"),
                            subtitle=ft.Text("Hello"),
                            trailing=ft.IconButton(icon=ft.Icons.DELETE_OUTLINE),
                        ),
                        ft.ListTile(
                            title=ft.Text("谢谢"),
                            subtitle=ft.Text("Thank you"),
                            trailing=ft.IconButton(icon=ft.Icons.DELETE_OUTLINE),
                        ),
                        ft.ListTile(
                            title=ft.Text("再见"),
                            subtitle=ft.Text("Goodbye"),
                            trailing=ft.IconButton(icon=ft.Icons.DELETE_OUTLINE),
                        ),
                    ],
                    expand=True,
                ),
            ],
            visible=False,
            scroll=ft.ScrollMode.AUTO,
        )

        # 切换侧边栏按钮
        self.toggle_button = ft.IconButton(
            icon=ft.Icons.ARROW_BACK, on_click=lambda e: self.app.toggle_left_sidebar()
        )

        # 主内容容器
        self.main_content = ft.Column(
            [
                ft.Row(
                    [ft.Text("Option"), self.toggle_button],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Divider(),
                self.nav_rail,
                ft.Divider(),
                self.settings_content,
                self.history_content,
            ],
            expand=True,
        )

        super().__init__(
            content=self.main_content,
            padding=ft.padding.all(15),
            margin=ft.margin.all(0),
            width=300,  # 稍微增加宽度以容纳更多内容
            bgcolor=ft.Colors.BLUE_GREY_50,
            expand=True,
        )

    def nav_change(self, e):
        index = e.control.selected_index
        if index == 0:  # 设置
            self.settings_content.visible = True
            self.history_content.visible = False
        elif index == 1:  # 历史
            self.settings_content.visible = False
            self.history_content.visible = True
        self.update()

    def save_settings(self, e):
        """保存设置按钮的点击事件处理函数"""
        print("=== 当前配置值 ===")
        print(f"API Key: {self.api_key_field.value}")
        print(f"Base URL: {self.base_url_field.value}")
        print(f"Model: {self.model_field.value}")
        print(f"Target Language: {self.target_language_field.value}")
        print(f"Reserved Word: {self.reserved_word_field.value}")
        print(f"自动检测语言: {self.auto_detect_switch.value}")
        print(f"发音功能: {self.pronunciation_switch.value}")
        print(f"保存翻译历史: {self.save_history_switch.value}")
        print("=================")

        # 显示保存成功的提示
        if self.app.page:
            self.app.page.snack_bar = ft.SnackBar(ft.Text("设置已保存!"))
            self.app.page.snack_bar.open = True
            self.app.page.update()

    def GenClient(self):
        LLM_Client = clientInfo(
            api_key=self.api_key_field.value,
            base_url=self.base_url_field.value,
            model=self.model_field.value,
            dryRun=False,
            local_cache=self.storage,
            usecache=self.save_history_switch.value,
        )
        print(f"自动检测语言: {self.auto_detect_switch.value}")
        print(f"发音功能: {self.pronunciation_switch.value}")
        print("=================")
        return LLM_Client

    def get_storage(self):
        return self.storage

    def getTranslationContext(self):
        context = TranslationContext(
            target_language=self.target_language_field.value,
            file_list="",
            configfile_path="",
            doc_folder="",
            reserved_word=self.reserved_word_field.value,
            max_files=20,
            disclaimers=False,
        )
        return context
