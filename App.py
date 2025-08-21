import flet as ft
import random
from datetime import datetime, timedelta

class TranslationApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "翻译应用"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.setup_ui()
        
        # 模拟统计数据
        self.translation_count = 42
        self.favorite_translations = 7
        self.generate_usage_data()
        
    def setup_ui(self):
        # 创建文本输入框
        self.text_input = ft.TextField(
            multiline=True,
            min_lines=5,
            max_lines=5,
            hint_text="请输入要翻译的文本...",
            expand=True,
            border_color=ft.Colors.BLUE_GREY_200
        )
        
        # 创建翻译按钮
        self.translate_btn = ft.ElevatedButton(
            "翻译",
            icon=ft.Icons.TRANSLATE,
            on_click=self.translate_text,
            style=ft.ButtonStyle(
                padding=20
            )
        )
        
        # 创建左侧边栏切换按钮（放在主内容区域）
        self.left_sidebar_toggle = ft.IconButton(
            icon=ft.Icons.MENU,
            tooltip="显示/隐藏设置",
            on_click=self.toggle_left_sidebar
        )
        
        # 创建右侧边栏切换按钮（放在主内容区域）
        self.right_sidebar_toggle = ft.IconButton(
            icon=ft.Icons.BAR_CHART,
            tooltip="显示/隐藏统计",
            on_click=self.toggle_right_sidebar
        )
        
        # 创建左侧边栏
        self.left_sidebar = LeftSidebar(self)
        
        # 创建右侧边栏
        self.right_sidebar = RightSidebar(self)
        
        # 创建主内容区域
        self.main_content = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("翻译工具", style=ft.TextThemeStyle.HEADLINE_LARGE),
                        self.left_sidebar_toggle,
                        self.right_sidebar_toggle
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                self.text_input,
                ft.Container(height=10),
                self.translate_btn,
                ft.Container(height=20),
                ft.Text("翻译结果:", style=ft.TextThemeStyle.HEADLINE_SMALL),
                ft.Container(
                    content=ft.Text("翻译结果将显示在这里...", style=ft.TextThemeStyle.BODY_LARGE),
                    padding=10,
                    border=ft.border.all(1, ft.Colors.BLUE_GREY_200),
                    border_radius=5,
                    width=self.page.width
                )
            ],
            alignment=ft.MainAxisAlignment.START,
            expand=True
        )
        
        # 设置页面布局
        self.page.add(
            ft.Row(
                [
                    self.left_sidebar,
                    ft.VerticalDivider(width=1, visible=False),
                    self.main_content,
                    ft.VerticalDivider(width=1, visible=False),
                    self.right_sidebar,
                ],
                expand=True,
            )
        )
    
    def toggle_left_sidebar(self,e=None):
        self.left_sidebar.visible = not self.left_sidebar.visible
        # 更新分割线的可见性
        self.page.controls[0].controls[1].visible = self.left_sidebar.visible
        # 更新按钮图标
        self.left_sidebar_toggle.icon = ft.Icons.MENU if not self.left_sidebar.visible else ft.Icons.ARROW_BACK
        self.page.update()
    
    def toggle_right_sidebar(self,e=None):
        self.right_sidebar.visible = not self.right_sidebar.visible
        # 更新分割线的可见性
        self.page.controls[0].controls[3].visible = self.right_sidebar.visible
        # 更新按钮图标
        self.right_sidebar_toggle.icon = ft.Icons.BAR_CHART if not self.right_sidebar.visible else ft.Icons.ARROW_FORWARD
        self.page.update()
    
    def translate_text(self, e):
        # 模拟翻译功能
        text = self.text_input.value
        if text:
            # 这里只是模拟翻译结果
            translations = {
                "你好": "Hello",
                "谢谢": "Thank you",
                "再见": "Goodbye",
                "早上好": "Good morning",
                "我爱你": "I love you"
            }
            
            # 尝试找到匹配的模拟翻译
            result = translations.get(text, "这是模拟的翻译结果")
            
            # 更新翻译结果
            self.main_content.controls[-1].content.value = result
            self.page.update()
    
    def generate_usage_data(self):
        # 生成模拟的使用数据
        self.usage_data = []
        for i in range(7):
            date = datetime.now() - timedelta(days=6-i)
            count = random.randint(1, 10)
            self.usage_data.append((date, count))
    
    def generate_bar_chart_data(self):
        # 生成柱状图数据
        groups = []
        colors = [ft.Colors.BLUE, ft.Colors.GREEN, ft.Colors.ORANGE, 
                 ft.Colors.RED, ft.Colors.PURPLE, ft.Colors.PINK, ft.Colors.INDIGO]
        self.usage_data = []
        for i in range(7):
            date = datetime.now() - timedelta(days=6-i)
            count = random.randint(1, 10)
            self.usage_data.append((date, count))
        for i, (date, count) in enumerate(self.usage_data):
            groups.append(
                ft.BarChartGroup(
                    x=i,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=count,
                            width=15,
                            color=colors[i],
                            tooltip=f"{date.strftime('%m/%d')}: {count}次",
                            border_radius=0,
                        )
                    ],
                )
            )
        return groups
    
    def generate_bottom_axis_labels(self):
        # 生成底部轴标签
        labels = []
        for date, _ in self.usage_data:
            labels.append(ft.ChartAxisLabel(
                value=self.usage_data.index((date, _)),
                label=ft.Text(date.strftime('%m/%d'))
            ))
        return labels


class LeftSidebar(ft.Container):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.visible = True
        
        # 创建导航项目
        self.nav_items = [
            ft.NavigationRailDestination(
                label_content=ft.Text("设置"),
                label="设置",
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
        
        # 创建设置内容
        self.settings_content = ft.Column(
            [
                ft.Text("翻译设置", style=ft.TextThemeStyle.HEADLINE_SMALL),
                ft.Divider(),
                ft.Text("目标语言:"),
                ft.Dropdown(
                    options=[
                        ft.dropdown.Option("英语"),
                        ft.dropdown.Option("法语"),
                        ft.dropdown.Option("德语"),
                        ft.dropdown.Option("日语"),
                        ft.dropdown.Option("韩语"),
                    ],
                    value="英语"
                ),
                ft.Text("翻译提供商:"),
                ft.Dropdown(
                    options=[
                        ft.dropdown.Option("Google 翻译"),
                        ft.dropdown.Option("百度翻译"),
                        ft.dropdown.Option("微软翻译"),
                        ft.dropdown.Option("DeepL"),
                    ],
                    value="Google 翻译"
                ),
                ft.Switch(label="自动检测语言", value=True),
                ft.Switch(label="发音功能", value=False),
                ft.Switch(label="保存翻译历史", value=True),
                ft.ElevatedButton("保存设置", icon=ft.Icons.SAVE)
            ],
            spacing=15
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
                            trailing=ft.IconButton(icon=ft.Icons.DELETE_OUTLINE)
                        ),
                        ft.ListTile(
                            title=ft.Text("谢谢"),
                            subtitle=ft.Text("Thank you"),
                            trailing=ft.IconButton(icon=ft.Icons.DELETE_OUTLINE)
                        ),
                        ft.ListTile(
                            title=ft.Text("再见"),
                            subtitle=ft.Text("Goodbye"),
                            trailing=ft.IconButton(icon=ft.Icons.DELETE_OUTLINE)
                        ),
                    ],
                    expand=True,
                )
            ],
            visible=False
        )
        
        # 切换侧边栏按钮
        self.toggle_button = ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            on_click=lambda e: self.app.toggle_left_sidebar()
        )
        
        super().__init__(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text("选项"),
                            self.toggle_button
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Divider(),
                    self.nav_rail,
                    ft.Divider(),
                    self.settings_content,
                    self.history_content
                ],
                tight=True,
            ),
            padding=ft.padding.all(15),
            margin=ft.margin.all(0),
            width=250,
            bgcolor=ft.Colors.BLUE_GREY_50,
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


class RightSidebar(ft.Container):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.visible = True
        
        # 切换侧边栏按钮
        self.toggle_button = ft.IconButton(
            icon=ft.Icons.ARROW_FORWARD,
            on_click=lambda e: self.app.toggle_right_sidebar()
        )
        
        super().__init__(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text("统计信息"),
                            self.toggle_button
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Divider(),
                    ft.Text(f"总翻译次数: 1"),
                    ft.Text(f"收藏翻译: 1"),
                    ft.Text("最近使用情况:"),
                    ft.Container(
                        content=ft.BarChart(
                            bar_groups=app.generate_bar_chart_data(),
                            border=ft.border.all(1, ft.Colors.GREY_400),
                            left_axis=ft.ChartAxis(
                                labels_size=40, title=ft.Text("次数")
                            ),
                            bottom_axis=ft.ChartAxis(
                                title=ft.Text("日期"),
                                labels=app.generate_bottom_axis_labels()
                            ),
                            horizontal_grid_lines=ft.ChartGridLines(
                                color=ft.Colors.GREY_300, width=1, dash_pattern=[3, 3]
                            ),
                            tooltip_bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLUE_GREY),
                            max_y=10,
                            interactive=True,
                            expand=True,
                        ),
                        height=200,
                    ),
                    ft.Text("常用翻译语言:"),
                    ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("语言")),
                            ft.DataColumn(ft.Text("次数")),
                        ],
                        rows=[
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(ft.Text("英语")),
                                    ft.DataCell(ft.Text("28")),
                                ]
                            ),
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(ft.Text("日语")),
                                    ft.DataCell(ft.Text("9")),
                                ]
                            ),
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(ft.Text("韩语")),
                                    ft.DataCell(ft.Text("5")),
                                ]
                            ),
                        ],
                    )
                ],
                spacing=15
            ),
            padding=ft.padding.all(15),
            margin=ft.margin.all(0),
            width=250,
            bgcolor=ft.Colors.BLUE_GREY_50,
        )


def main(page: ft.Page):
    app = TranslationApp(page)

ft.app(target=main)