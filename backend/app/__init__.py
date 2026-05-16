"""
Seeus Backend - Flask应用工厂
"""

import os
import warnings

# 抑制 multiprocessing resource_tracker 的警告（来自第三方库如 transformers）
# 需要在所有其他导入之前设置
warnings.filterwarnings("ignore", message=".*resource_tracker.*")

from flask import Flask, request
from flask_cors import CORS

from .config import Config
from .utils.logger import setup_logger, get_logger


def create_app(config_class=Config):
    """Flask应用工厂函数"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 设置JSON编码：确保中文直接显示（而不是 \uXXXX 格式）
    # Flask >= 2.3 使用 app.json.ensure_ascii，旧版本使用 JSON_AS_ASCII 配置
    if hasattr(app, 'json') and hasattr(app.json, 'ensure_ascii'):
        app.json.ensure_ascii = False
    
    # 设置日志
    logger = setup_logger('seeus')
    
    # 只在 reloader 子进程中打印启动信息（避免 debug 模式下打印两次）
    is_reloader_process = os.environ.get('WERKZEUG_RUN_MAIN') == 'true'
    debug_mode = app.config.get('DEBUG', False)
    should_log_startup = not debug_mode or is_reloader_process
    
    if should_log_startup:
        logger.info("=" * 50)
        logger.info("Seeus Backend 启动中...")
        logger.info("=" * 50)
    
    # 启用CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Legacy MiroFish simulation cleanup — dormant. Re-enable by reinstating
    # camel-ai / camel-oasis / zep-cloud in requirements.txt.
    # from .services.simulation_runner import SimulationRunner
    # SimulationRunner.register_cleanup()
    
    # 请求日志中间件
    @app.before_request
    def log_request():
        logger = get_logger('seeus.request')
        logger.debug(f"请求: {request.method} {request.path}")
        if request.content_type and 'json' in request.content_type:
            logger.debug(f"请求体: {request.get_json(silent=True)}")
    
    @app.after_request
    def log_response(response):
        logger = get_logger('seeus.request')
        logger.debug(f"响应: {response.status_code}")
        return response
    
    # Local lead store (SQLite) — single source of truth for captured emails.
    # Idempotent: creates the table on first boot, no-op after that.
    from .services.lead_store import init_db as init_lead_store
    init_lead_store()

    # Register active blueprints. Legacy blueprints (graph/simulation/report)
    # are commented out — see app/api/__init__.py for details.
    from .api import label_bp, checklist_bp, admin_bp
    app.register_blueprint(label_bp, url_prefix='/api/label')
    app.register_blueprint(checklist_bp, url_prefix='/api/checklist')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    
    # 健康检查
    @app.route('/health')
    def health():
        return {'status': 'ok', 'service': 'Seeus Backend'}
    
    if should_log_startup:
        logger.info("Seeus Backend 启动完成")
    
    return app

