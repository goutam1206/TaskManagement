import streamlit as st
from DeleteTask import deleteTask
from CreateTask import createTask
from SearchTask import searchTask

st.title("Task Manager")

def landingPage():
    st.set_page_config(page_title="Task Management Dashboard", layout="wide", )
    taskActivities : {
        "Task Manager" : showPage,
        "Create Task" : createTask,
        "Search Task" : searchTask,
        "Delete Task" : deleteTask
    }
    selected_activity = st.sidebar.radio("Task Facets", list(taskActivities.keys()))


def showPage():
    st.header("Welcome to the Task Management application")


if __name__ == "__main__":
    st.session_state.page = "Task Manager"
    landingPage()