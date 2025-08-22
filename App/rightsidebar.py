import flet as ft


class RightSidebar(ft.Container):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.visible = True

        # 切换侧边栏按钮
        self.toggle_button = ft.IconButton(
            icon=ft.Icons.ARROW_FORWARD,
            on_click=lambda e: self.app.toggle_right_sidebar(),
        )

        super().__init__(
            content=ft.Column(
                [
                    ft.Row(
                        [ft.Text("统计信息"), self.toggle_button],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Divider(),
                    ft.Text("总翻译次数: 1"),
                    ft.Text("收藏翻译: 1"),
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
                                labels=app.generate_bottom_axis_labels(),
                            ),
                            horizontal_grid_lines=ft.ChartGridLines(
                                color=ft.Colors.GREY_300, width=1, dash_pattern=[3, 3]
                            ),
                            tooltip_bgcolor=ft.Colors.with_opacity(
                                0.8, ft.Colors.BLUE_GREY
                            ),
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
                    ),
                ],
                spacing=15,
            ),
            padding=ft.padding.all(15),
            margin=ft.margin.all(0),
            width=250,
            bgcolor=ft.Colors.BLUE_GREY_50,
        )
