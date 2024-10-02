from todo_backend.Todo import Todo


class TodoRepository:
    def __init__(self):
        self.todos = {
            1: Todo(id=1, title="Buy Milk", description="Buy Milk from the store"),
            2: Todo(id=2, title="Buy Bread", description="Buy Bread from the store")
        }
    
    def get_all_todos(self):
        return self.todos.values()
    
    def get_todo_by_id(self, todo_id):
        return self.todos.get(todo_id)