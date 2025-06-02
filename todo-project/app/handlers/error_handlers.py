from werkzeug.exceptions import HTTPException, NotFound, InternalServerError

def error_handlers(app):
    """エラーハンドラーの登録"""
    from flask import render_template, request
    
    @app.errorhandler(NotFound)
    def page_not_found(e):
        """404エラー"""
        return render_template('error/not_found.html'), 404
    
    @app.errorhandler(InternalServerError)
    def internal_server_error(e):
        """500エラー"""
        app.logger.error(f"500エラー: {str(e)}")
        return render_template('error/internal_server.html'), 500
