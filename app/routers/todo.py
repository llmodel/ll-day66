from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from dependencies import get_session
from models.todo import ToDo
from schemas.todo import ToDoCreate, ToDoUpdate, ToDoResponse

router = APIRouter(prefix="/todos", tags=["ToDo"])

@router.post("/", response_model=ToDoResponse)
def create_todo(todo: ToDoCreate, session: Session = Depends(get_session)):
    '''
    Create a new ToDo item
    '''
    new_todo = ToDo(**todo.dict())
    session.add(new_todo)
    session.commit()
    session.refresh(new_todo)
    return new_todo

@router.get("/{todo_id}", response_model=ToDoResponse)
def get_todo(todo_id: int, session: Session = Depends(get_session)):
    '''
    Get a ToDo item by ID
    '''
    todo = session.get(ToDo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo not found")
    return todo

@router.get("/", response_model=list[ToDoResponse])
def get_todos(session: Session = Depends(get_session)):
    '''
    Get all ToDo items
    '''
    todos = session.exec(select(ToDo)).all()
    return todos

@router.put("/{todo_id}", response_model=ToDoResponse)
def update_todo(todo_id: int, todo_update: ToDoUpdate, session: Session = Depends(get_session)):
    '''
    Update a ToDo item by ID
    '''
    todo = session.get(ToDo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo not found")

    todo_data = todo_update.model_dump(exclude_unset=True)
    for key, value in todo_data.items():
        setattr(todo, key, value)

    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

@router.delete("/{todo_id}")
def delete_todo(todo_id: int, session: Session = Depends(get_session)):
    '''
    Delete a ToDo item by ID
    '''
    todo = session.get(ToDo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo not found")
    
    session.delete(todo)
    session.commit()
    return {"detail": "ToDo deleted successfully"}