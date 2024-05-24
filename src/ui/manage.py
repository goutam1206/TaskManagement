import streamlit as st
from DeleteTask import deleteTask
from CreateTask import createTask
from SearchTask import searchTask



def landingPage():
    st.set_page_config(page_title="Task Management Dashboard", layout="wide", )
    st.title("Task Manager")
    taskActivities = {
        "Task Manager" : showPage,
        "Create Task" : createTask,
        "Search Task" : searchTask,
        "Delete Task" : deleteTask
    }
    selected_activity = st.sidebar.radio("Task Facets", list(taskActivities.keys()))
    taskActivities[selected_activity]()


def showPage():
    st.header("Welcome to the Task Management application")


if __name__ == "__main__":
    st.session_state.page = "Task Manager"
    landingPage()