import streamlit as st
import time
from datetime import datetime, timedelta
import pygame

# Initialize pygame mixer for sound
pygame.mixer.init()

st.set_page_config(page_title="Pomodoro Timer", page_icon="🍅", layout="centered")

# Custom CSS for better styling
st.markdown("""
<style>
    .big-timer {
        font-size: 80px;
        font-weight: bold;
        text-align: center;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
    .work-session {
        background-color: #ff6b6b;
        color: white;
    }
    .break-session {
        background-color: #4ecdc4;
        color: white;
    }
    .session-info {
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        margin: 10px 0;
    }
    .stats-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

st.title("🍅 Pomodoro Timer")
st.write("Stay focused and productive with the Pomodoro Technique!")

# Initialize session state
if 'timer_running' not in st.session_state:
    st.session_state.timer_running = False
if 'time_left' not in st.session_state:
    st.session_state.time_left = 25 * 60  # 25 minutes in seconds
if 'session_type' not in st.session_state:
    st.session_state.session_type = 'work'  # 'work', 'short_break', 'long_break'
if 'completed_pomodoros' not in st.session_state:
    st.session_state.completed_pomodoros = 0
if 'total_focus_time' not in st.session_state:
    st.session_state.total_focus_time = 0
if 'last_update' not in st.session_state:
    st.session_state.last_update = time.time()

# Settings in sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    work_duration = st.slider("Work Duration (minutes)", 15, 60, 25, 5)
    short_break_duration = st.slider("Short Break (minutes)", 3, 10, 5, 1)
    long_break_duration = st.slider("Long Break (minutes)", 15, 30, 15, 5)
    pomodoros_until_long_break = st.slider("Pomodoros until Long Break", 2, 6, 4, 1)
    
    st.divider()
    
    st.header("📊 Today's Stats")
    st.metric("Completed Pomodoros", st.session_state.completed_pomodoros)
    hours = st.session_state.total_focus_time // 3600
    minutes = (st.session_state.total_focus_time % 3600) // 60
    st.metric("Total Focus Time", f"{int(hours)}h {int(minutes)}m")
    
    st.divider()
    
    if st.button("🔄 Reset Stats", use_container_width=True):
        st.session_state.completed_pomodoros = 0
        st.session_state.total_focus_time = 0
        st.rerun()

# Function to play sound (placeholder - add your own sound file)
def play_sound():
    try:
        # You can replace this with a custom sound file
        # pygame.mixer.music.load("notification.mp3")
        # pygame.mixer.music.play()
        st.toast("⏰ Session Complete!", icon="🎉")
    except:
        pass

# Format time display
def format_time(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

# Timer logic
if st.session_state.timer_running:
    current_time = time.time()
    elapsed = current_time - st.session_state.last_update
    st.session_state.time_left -= elapsed
    st.session_state.last_update = current_time
    
    # Update focus time if work session
    if st.session_state.session_type == 'work':
        st.session_state.total_focus_time += elapsed
    
    # Check if time is up
    if st.session_state.time_left <= 0:
        play_sound()
        
        # Transition to next session
        if st.session_state.session_type == 'work':
            st.session_state.completed_pomodoros += 1
            
            # Determine break type
            if st.session_state.completed_pomodoros % pomodoros_until_long_break == 0:
                st.session_state.session_type = 'long_break'
                st.session_state.time_left = long_break_duration * 60
                st.balloons()
            else:
                st.session_state.session_type = 'short_break'
                st.session_state.time_left = short_break_duration * 60
        else:
            st.session_state.session_type = 'work'
            st.session_state.time_left = work_duration * 60
        
        st.session_state.timer_running = False

# Display current session type
session_names = {
    'work': '💼 Work Session',
    'short_break': '☕ Short Break',
    'long_break': '🌟 Long Break'
}

session_colors = {
    'work': 'work-session',
    'short_break': 'break-session',
    'long_break': 'break-session'
}

st.markdown(f'<p class="session-info">{session_names[st.session_state.session_type]}</p>', unsafe_allow_html=True)

# Display timer
timer_class = session_colors[st.session_state.session_type]
st.markdown(f'<div class="big-timer {timer_class}">{format_time(st.session_state.time_left)}</div>', unsafe_allow_html=True)

# Progress bar
if st.session_state.session_type == 'work':
    total_time = work_duration * 60
elif st.session_state.session_type == 'short_break':
    total_time = short_break_duration * 60
else:
    total_time = long_break_duration * 60

progress = max(0, min(1, (total_time - st.session_state.time_left) / total_time))
st.progress(progress)

# Control buttons
col1, col2, col3 = st.columns(3)

with col1:
    if not st.session_state.timer_running:
        if st.button("▶️ Start", use_container_width=True, type="primary"):
            st.session_state.timer_running = True
            st.session_state.last_update = time.time()
            st.rerun()
    else:
        if st.button("⏸️ Pause", use_container_width=True):
            st.session_state.timer_running = False
            st.rerun()

with col2:
    if st.button("⏭️ Skip", use_container_width=True):
        if st.session_state.session_type == 'work':
            st.session_state.session_type = 'short_break'
            st.session_state.time_left = short_break_duration * 60
        else:
            st.session_state.session_type = 'work'
            st.session_state.time_left = work_duration * 60
        st.session_state.timer_running = False
        st.rerun()

with col3:
    if st.button("🔄 Reset", use_container_width=True):
        if st.session_state.session_type == 'work':
            st.session_state.time_left = work_duration * 60
        elif st.session_state.session_type == 'short_break':
            st.session_state.time_left = short_break_duration * 60
        else:
            st.session_state.time_left = long_break_duration * 60
        st.session_state.timer_running = False
        st.rerun()

# Task list section
st.divider()
st.subheader("📝 Today's Tasks")

if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# Add new task
new_task = st.text_input("Add a new task", placeholder="What are you working on?")
if st.button("➕ Add Task") and new_task:
    st.session_state.tasks.append({'task': new_task, 'completed': False})
    st.rerun()

# Display tasks
if st.session_state.tasks:
    for idx, task_item in enumerate(st.session_state.tasks):
        col1, col2 = st.columns([4, 1])
        with col1:
            is_done = st.checkbox(
                task_item['task'],
                value=task_item['completed'],
                key=f"task_{idx}",
                label_visibility="visible"
            )
            if is_done != task_item['completed']:
                st.session_state.tasks[idx]['completed'] = is_done
                st.rerun()
        with col2:
            if st.button("🗑️", key=f"delete_{idx}"):
                st.session_state.tasks.pop(idx)
                st.rerun()
else:
    st.info("No tasks yet. Add one above to get started!")

# Auto-refresh when timer is running
if st.session_state.timer_running:
    time.sleep(0.1)
    st.rerun()

# Tips section
with st.expander("💡 Pomodoro Tips"):
    st.write("""
    **How to use the Pomodoro Technique:**
    1. Choose a task to work on
    2. Set the timer for 25 minutes (1 Pomodoro)
    3. Work on the task until the timer rings
    4. Take a 5-minute break
    5. After 4 Pomodoros, take a longer 15-minute break
    
    **Best Practices:**
    - Eliminate all distractions before starting
    - If you finish early, use remaining time to review
    - Don't check phone/email during work sessions
    - Use breaks to rest your eyes and move around
    - Stay hydrated!
    """)
