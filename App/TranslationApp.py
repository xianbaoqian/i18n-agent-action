import random
from datetime import datetime, timedelta
import flet as ft
import pyttsx3
import os
import sys
# 添加项目根目录到Python路径
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from AgentUtils.span import Span_Mgr  # noqa: E402
from Business.translate import translateAgent  # noqa: E402

from leftsidebar import LeftSidebar
from rightsidebar import RightSidebar

class TranslationApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "i18n agent"
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
            border_color=ft.Colors.BLUE_GREY_200,
        )

        # 创建翻译按钮
        self.translate_btn = ft.ElevatedButton(
            "Translate",
            icon=ft.Icons.TRANSLATE,
            on_click=self.translate_text,
            style=ft.ButtonStyle(padding=20),
        )

        # 创建左侧边栏切换按钮（放在主内容区域）
        self.left_sidebar_toggle = ft.IconButton(
            icon=ft.Icons.MENU,
            tooltip="显示/隐藏设置",
            on_click=self.toggle_left_sidebar,
        )

        # 创建右侧边栏切换按钮（放在主内容区域）
        self.right_sidebar_toggle = ft.IconButton(
            icon=ft.Icons.BAR_CHART,
            tooltip="显示/隐藏统计",
            on_click=self.toggle_right_sidebar,
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
                        ft.Text("i18n agent", style=ft.TextThemeStyle.HEADLINE_LARGE),
                        self.left_sidebar_toggle,
                        self.right_sidebar_toggle,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                self.text_input,
                ft.Container(height=10),
                self.translate_btn,
                ft.Container(height=20),
                ft.Text("Translate result:", style=ft.TextThemeStyle.HEADLINE_SMALL),
                ft.Container(
                    content=ft.Text(
                        "Translate result...", style=ft.TextThemeStyle.BODY_LARGE
                    ),
                    padding=10,
                    border=ft.border.all(1, ft.Colors.BLUE_GREY_200),
                    border_radius=5,
                    width=self.page.width,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            expand=True,
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

    def toggle_left_sidebar(self, e=None):
        self.left_sidebar.visible = not self.left_sidebar.visible
        # 更新分割线的可见性
        self.page.controls[0].controls[1].visible = self.left_sidebar.visible
        # 更新按钮图标
        self.left_sidebar_toggle.icon = (
            ft.Icons.MENU if not self.left_sidebar.visible else ft.Icons.ARROW_BACK
        )
        self.page.update()

    def toggle_right_sidebar(self, e=None):
        self.right_sidebar.visible = not self.right_sidebar.visible
        # 更新分割线的可见性
        self.page.controls[0].controls[3].visible = self.right_sidebar.visible
        # 更新按钮图标
        self.right_sidebar_toggle.icon = (
            ft.Icons.BAR_CHART
            if not self.right_sidebar.visible
            else ft.Icons.ARROW_FORWARD
        )
        self.page.update()

    def translate_text(self, e):
        # 模拟翻译功能
        LLM_client = self.left_sidebar.GenClient()
        storage = self.left_sidebar.get_storage()
        context = self.left_sidebar.getTranslationContext()
        span_mgr = Span_Mgr(storage)
        root_span = span_mgr.create_span("Root operation")
        TsAgent = translateAgent(LLM_client, span_mgr)
        text = self.text_input.value
        print(text)
        engine = pyttsx3.init()

        if text:
            # 尝试找到匹配的模拟翻译
            result = TsAgent.translate(
                context, context.target_language, text, root_span
            )
            print(result)
            # 更新翻译结果
            self.main_content.controls[-1].content.value = result
            self.page.update()
            engine.say(result)
            # play the speech
            engine.runAndWait()

    def generate_usage_data(self):
        # 生成模拟的使用数据
        self.usage_data = []
        for i in range(7):
            date = datetime.now() - timedelta(days=6 - i)
            count = random.randint(1, 10)
            self.usage_data.append((date, count))

    def generate_bar_chart_data(self):
        # 生成柱状图数据
        groups = []
        colors = [
            ft.Colors.BLUE,
            ft.Colors.GREEN,
            ft.Colors.ORANGE,
            ft.Colors.RED,
            ft.Colors.PURPLE,
            ft.Colors.PINK,
            ft.Colors.INDIGO,
        ]
        self.usage_data = []
        for i in range(7):
            date = datetime.now() - timedelta(days=6 - i)
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
            labels.append(
                ft.ChartAxisLabel(
                    value=self.usage_data.index((date, _)),
                    label=ft.Text(date.strftime("%m/%d")),
                )
            )
        return labels