"""メッセージ文字列の定数を管理"""

# --- Flash Messages ---

FLASH_MESSAGES = {
    "authentication": {
        "USER_REGISTERED_SUCCESS": "ユーザー登録が完了しました。ログインしてください。",
        "USER_REGISTERED_ERROR": "ユーザー登録に失敗しました。再度入力してください。",
        "USER_LOGIN_ERROR": "メールアドレスまたはパスワードが間違っています。",
        "USER_LOGIN_EXCEPTION": "ログイン処理中にエラーが発生しました。",
        "USER_LOGOUT_SUCCESS": "ログアウトしました。"
    },
    "todos": {
        "CREATED_SUCCESS": "TODOの作成が完了しました。",
        "CREATED_ERROR": "TODOの作成に失敗しました。再度入力してください。",
        "UPDATED_SUCCESS": "TODOを更新しました。",
        "DELETED_SUCCESS": "TODO「{}」を削除しました。",
        "DELETE_ERROR": "TODOの削除に失敗しました。",
        "FETCH_ERROR": "Todo情報の取得に失敗しました。",
        "NOT_FOUND": "指定されたTODOは見つかりませんでした。"
    },
    "users": {
        "UPDATED_SUCCESS": "ユーザー情報を更新しました。",
        "DELETE_FAILED": "ユーザー情報の削除が出来ませんでした。",
        "INFO_FETCH_ERROR": "ユーザー情報の取得に失敗しました。",
        "ID_NOT_FOUND": "ユーザーID {} の情報は見つかりませんでした。"
    },
    "general": {
        "LOGIN_REQUIRED": "ログインしてください。"
    }
}

# --- Error Messages (for exceptions, typically logged or for internal use) ---

ERROR_MESSAGES = {
    "user_model": {
        "REGISTRATION_FAILED": "ユーザー情報の登録に失敗しました。",
        "FETCH_FAILED": "ユーザー情報の取得に失敗しました。",
        "FETCH_BY_ID_FAILED": "idによるユーザー情報の取得に失敗しました。",
        "UPDATE_FAILED": "ユーザー情報の更新に失敗しました。",
        "DELETE_FAILED": "ID:{}のユーザー情報の削除に失敗しました。",
        "USER_ID_NOT_FOUND": "User with id {} not found",
    },
    "todos_model": {
        "FETCH_FAILED": "Todo情報の取得に失敗しました。",
        "INSERT_FAILED": "Todo情報の作成に失敗しました。",
        "GET_BY_ID_FAILED": "ID:{}のTodo情報の獲得に失敗しました。",
        "UPDATE_FAILED": "ID:{}のTodo情報の獲得に失敗しました。",
        "DELETE_FAILED": "ID:{}のTodo情報の削除に失敗しました。",
        "TODO_ID_NOT_FOUND": "Todo with id {} not found",
    }
}
