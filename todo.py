from pathlib import Path
from os import remove
from json import load,dump
import click


@click.command()
@click.option('--create', '-c', is_flag=True, help='Create a to-do list.')
@click.option('--add', '-a', default = 0, type = click.IntRange(0, 5, clamp=True), 
    help = 'Add the specified number of to-dos.')
@click.option('--done', '-d', type = tuple, help = 'Tag to-dos you have done.')
@click.option('--delete', '-x', is_flag = True, help = 'Delete the to-do list.')
def todo_command(create, add, done : tuple, delete):
    """
    A simple tools to create a to-do list in command line.\n
    Just type 'todo' in terminal to see the to-do list you have created.
    """

    path = Path("todolist.txt")

    if create:
        create_todo_list(path)
    elif add > 0:
        add_todo_list(path,add)
    elif done:
        done_todo(path,done)
    elif delete:
        remove(path)
    else:
        if path.exists():
            dic_todo = read_json(path)
            for k,v in dic_todo.items():
                click.echo(f"{k}.{v[0]}")
                if v[1]:click.echo(click.style('[Done]', fg = 'green'))
                else:click.echo(click.style('[Todo]', fg = 'red'))
        else:
            click.echo('To-do list is not exist,\n \
                please create first by using the "-c" option.')

def create_todo_list(path : Path):
    if path.exists() and not click.confirm(
        'Already exist a to-do list.\n\
            Do you want to create a new one?'
            ):
        return
    click.echo(click.style('enter "exit" to finish this to-do list.', fg = ''))
    todolists = [""]
    i = 1
    while 'exit' not in todolists[-1]:
        todolists.append(click.prompt(f"{i}.",type = str))
        i += 1
    #print(todolists[1:-1])
    dic_todo = {}
    for j in range(i-2):
        dic_todo[j+1] = [todolists[j+1],False]
    write_json(path, dic_todo)

def add_todo_list(path : Path, num : int):
    if not path.exists():
        if click.confirm('To-do list has not been created.\n \
            Do you want to create now?'):
            create_todo_list(path)
        else:
            return
    else:
        dic_todo = read_json(path)
        todo_len = len(dic_todo)
        for i in range(todo_len + 1, todo_len + num + 1):
            dic_todo[i] = [click.prompt(f"{i}.",type = str),False]
        write_json(path, dic_todo)

def done_todo(path : Path, done : tuple):
    if not path.exists():
        if click.confirm('To-do list has not been created.\n \
            Do you want to create now?'):
            create_todo_list(path)
        else:
            return
    else:
        dic_todo = read_json(path)
        for k in done:
            if k in dic_todo:
                dic_todo[k][1] = True
        write_json(path, dic_todo)

def read_json(path : Path) -> dict:
    with open(path,'r',encoding='utf-8') as f:
        dic_todo : dict = load(f)
    return dic_todo

def write_json(path : Path, dic : dict):
    with open(path,'w',encoding = 'utf-8') as f:
        dump(dic,f) 
