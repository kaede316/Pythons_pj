from nicegui import ui
from nicegui.events import MouseEventArguments


# 用户类用于存储状态
class UserState:
    def __init__(self):
        self.sidebar_expanded = True
        self.visited_pages = []


user = UserState()

# 工具数据
tools = [
    {"id": "data_processor", "name": "数据处理工具", "icon": "settings", "description": "用于清洗、转换和分析数据",
     "category": "data", "color": "blue"},
    {"id": "chart_maker", "name": "图表生成器", "icon": "bar_chart", "description": "创建各种类型的统计图表",
     "category": "visualization", "color": "green"},
    {"id": "text_analyzer", "name": "文本分析", "icon": "text_fields", "description": "分析文本内容并提取关键信息",
     "category": "analysis", "color": "purple"},
    {"id": "image_editor", "name": "图像编辑器", "icon": "image", "description": "编辑和处理图像文件",
     "category": "media", "color": "orange"},
    {"id": "code_formatter", "name": "代码格式化", "icon": "code", "description": "格式化各种编程语言的代码",
     "category": "development", "color": "red"},
    {"id": "file_converter", "name": "文件转换器", "icon": "transform", "description": "在不同格式之间转换文件",
     "category": "utilities", "color": "teal"},
    {"id": "stats_calculator", "name": "统计计算器", "icon": "calculate", "description": "执行各种统计计算和分析",
     "category": "analysis", "color": "indigo"},
    {"id": "data_extractor", "name": "数据提取器", "icon": "cloud_download", "description": "从各种来源提取数据",
     "category": "data", "color": "blue"},
]


# 创建工具详情页面
def create_tool_pages():
    for tool in tools:
        current_tool = tool

        @ui.page(f'/tool/{current_tool["id"]}')
        def tool_page():
            if f'/tool/{current_tool["id"]}' not in user.visited_pages:
                user.visited_pages.append(f'/tool/{current_tool["id"]}')

            with ui.header().classes('bg-blue-100 text-black shadow-md'):
                with ui.row().classes('w-full items-center justify-between'):
                    ui.button(icon='arrow_back', on_click=lambda: ui.open('/')).props('flat')
                    ui.label(f"工具详情: {current_tool['name']}").classes('text-xl font-bold')
                    ui.space()

            with ui.column().classes('w-full p-8 max-w-6xl mx-auto'):
                with ui.row().classes('w-full items-start gap-8'):
                    with ui.column().classes('flex-shrink-0'):
                        ui.icon(current_tool['icon'], size='xl', color=current_tool['color']).classes('text-6xl')

                    with ui.column().classes('flex-grow'):
                        ui.label(current_tool['name']).classes('text-3xl font-bold mb-4')
                        ui.label(current_tool['description']).classes('text-lg text-gray-700 mb-6')

                        with ui.row().classes('gap-4'):
                            ui.button('启动工具', icon='play_arrow', color='primary')
                            ui.button('使用教程', icon='menu_book', color='secondary')

                ui.separator().classes('my-8')

                with ui.column().classes('w-full'):
                    ui.label('工具功能特性').classes('text-2xl font-bold mb-6')
                    with ui.grid(columns=2).classes('w-full gap-4'):
                        with ui.card().classes('p-4'):
                            ui.label('核心功能').classes('text-xl font-semibold mb-2')
                            ui.label('提供强大的数据处理能力，支持多种数据格式和转换操作。')
                        with ui.card().classes('p-4'):
                            ui.label('性能指标').classes('text-xl font-semibold mb-2')
                            ui.label('处理速度高达每秒万条记录，支持实时数据流处理。')


# 创建工具页面
create_tool_pages()


# 主页面
@ui.page('/')
def main_page():
    with ui.header().classes('bg-blue-600 text-white shadow-lg'):
        with ui.row().classes('w-full items-center justify-between'):
            with ui.row().classes('items-center gap-4'):
                ui.icon('widgets', size='lg', color='white')
                ui.label('工具平台').classes('text-xl font-bold')

            with ui.row().classes('items-center gap-2'):
                ui.button(icon='search', color='blue').props('flat')
                ui.button(icon='notifications', color='blue').props('flat')
                ui.button(icon='account_circle', color='blue').props('flat')

    with ui.row().classes('w-full h-full'):
        with ui.column().classes('h-full bg-lime-100 shadow-md transition-all duration-300') \
                .bind_visibility_from(user, 'sidebar_expanded'):
            with ui.column().classes('p-4 w-64'):
                ui.label('工具分类').classes('text-lg font-bold mb-4 mt-2')

                categories = ['所有工具', '数据分析', '可视化', '媒体处理', '开发工具', '实用工具']
                for category in categories:
                    ui.button(category, icon='folder', color='blue') \
                        .props('flat align=left') \
                        .classes('w-full justify-start mb-1')

                ui.space().classes('my-4')
                ui.separator()
                ui.space().classes('my-4')

                ui.button('设置', icon='settings', color='blue').props('flat align=left').classes(
                    'w-full justify-start')
                ui.button('帮助', icon='help', color='blue').props('flat align=left').classes('w-full justify-start')

        with ui.column().classes('flex-grow p-0'):
            with ui.row().classes('w-full items-center justify-between mb-8'):
                ui.label('所有工具').classes('text-xl font-bold')
                with ui.row().classes('items-center'):
                    with ui.row().classes('items-center w-64 border-none'):
                        ui.icon('search', color='green').classes('ml-2')
                        ui.input('搜索工具').classes('flex-grow border-none')
                    ui.toggle(['最近使用', '最受欢迎', 'A-Z排序'], value='最近使用')

            with ui.grid(columns=4).classes('w-full gap-6'):
                for tool in tools:
                    with ui.card().classes('w-full h-48 relative flex items-center justify-center group cursor-pointer') \
                            .on('click', lambda _, tool_id=tool['id']: ui.open(f'/tool/{tool_id}')):
                        with ui.column().classes('flex items-center justify-center text-center w-full h-full'):
                            ui.icon(tool['icon'], size='xl', color=tool['color']).classes('text-4xl mb-2')
                            ui.label(tool['name']).classes('font-semibold')

                        with ui.column().classes(
                                'absolute inset-0 bg-white bg-opacity-90 opacity-0 group-hover:opacity-100 transition-opacity duration-300 p-4 rounded shadow-lg flex items-center justify-center text-center'):
                            ui.label(tool['name']).classes('text-lg font-bold text-center mb-2')
                            ui.label(tool['description']).classes('text-gray-700 text-center mb-4')
                            with ui.row().classes('justify-center'):
                                ui.badge(tool['category']).props('color=%s' % tool['color'])
                            with ui.row().classes('absolute bottom-4 left-0 right-0 justify-center'):
                                ui.button('查看详情', icon='visibility', color='primary').props('small')

    with ui.footer().classes('bg-gray-800 text-white p-4 text-center'):
        ui.label('© 2025 工具平台 - kaede 所有权利保留').classes('text-sm')


# 启动应用
ui.run(title='工具导航平台', reload=False, binding_refresh_interval=0.1)