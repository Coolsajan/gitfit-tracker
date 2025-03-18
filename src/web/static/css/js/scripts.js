// DOM Elements
const videoFeed = document.getElementById('video-feed');
const exerciseName = document.getElementById('exercise-name');
const exerciseStatus = document.getElementById('exercise-status');
const currentTime = document.getElementById('current-time');
const totalTime = document.getElementById('total-time');
const calories = document.getElementById('calories');
const totalReps = document.getElementById('total-reps');
const setsCompleted = document.getElementById('sets-completed');
const currentRep = document.getElementById('current-rep');
const currentSet = document.getElementById('current-set');
const formScore = document.getElementById('form-score');
const repProgress = document.getElementById('rep-progress');
const setProgress = document.getElementById('set-progress');
const formProgress = document.getElementById('form-progress');
const workoutList = document.getElementById('workout-list');

// Buttons
const startBtn = document.getElementById('start-btn');
const pauseBtn = document.getElementById('pause-btn');
const stopBtn = document.getElementById('stop-btn');

// Sample workout data (replace with your actual workout data)
const workoutPlan = [
    { name: "Jumping Jacks", sets: 3, reps: 15, status: "upcoming" },
    { name: "Squats", sets: 4, reps: 12, status: "upcoming" },
    { name: "Push-ups", sets: 3, reps: 10, status: "upcoming" },
    { name: "Lunges", sets: 3, reps: 12, status: "upcoming" },
    { name: "Lunges", sets: 3, reps: 12, status: "upcoming" }
];

// Workout state
let workoutActive = false;
let currentExerciseIndex = 0;
let workoutTimer = null;
let elapsedSeconds = 0;

// Initialize the UI
function initializeUI() {
    renderWorkoutPlan();
    updateClock();
    setInterval(updateClock, 1000);
}

// Update the current time display
function updateClock() { 
    const now = new Date();
    currentTime.textContent = now.toLocaleTimeString();
}

// Render the workout plan
function renderWorkoutPlan() {
    workoutList.innerHTML = '';
    
    workoutPlan.forEach((exercise, index) => {
        const exerciseItem = document.createElement('div');
        exerciseItem.className = `workout-item ${index === currentExerciseIndex && workoutActive ? 'current' : ''}`;
        
        exerciseItem.innerHTML = `
            <div>
                <div class="workout-name">${exercise.name}</div>
                <div class="workout-details">${exercise.status}</div>
            </div>
            <div>${exercise.sets} × ${exercise.reps}</div>
        `;
        
        workoutList.appendChild(exerciseItem);
    });
}

// Update workout timer
function updateWorkoutTimer() {
    elapsedSeconds++;
    const minutes = Math.floor(elapsedSeconds / 60);
    const seconds = elapsedSeconds % 60;
    totalTime.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
}

// Start workout
function startWorkout() {
    workoutActive = true;
    exerciseStatus.textContent = 'In Progress';
    
    // Set first exercise as current
    workoutPlan[currentExerciseIndex].status = 'in progress';
    exerciseName.textContent = workoutPlan[currentExerciseIndex].name;
    
    // Start timer
    if (!workoutTimer) {
        workoutTimer = setInterval(updateWorkoutTimer, 1000);
    }
    
    renderWorkoutPlan();
    
    // This is where you would start your OpenCV/MediaPipe tracking
    // For example: startTracking();
}

// Pause workout
function pauseWorkout() {
    workoutActive = false;
    exerciseStatus.textContent = 'Paused';
    
    // Stop timer
    clearInterval(workoutTimer);
    workoutTimer = null;
    
    // This is where you would pause your OpenCV/MediaPipe tracking
    // For example: pauseTracking();
}

// Stop workout
function stopWorkout() {
    workoutActive = false;
    exerciseStatus.textContent = 'Stopped';
    
    // Reset timer
    clearInterval(workoutTimer);
    workoutTimer = null;
    elapsedSeconds = 0;
    totalTime.textContent = '00:00';
    
    // Reset exercise statuses
    workoutPlan.forEach(exercise => {
        exercise.status = 'upcoming';
    });
    
    renderWorkoutPlan();
    
    // This is where you would stop your OpenCV/MediaPipe tracking
    // For example: stopTracking();
}

// Update metrics (call this from your OpenCV/MediaPipe code)
function updateMetrics(data) {
    // Example data structure:
    // data = {
    //     currentRep: 5,
    //     totalReps: 12,
    //     currentSet: 2,
    //     totalSets: 4,
    //     formScore: 95,
    //     totalRepsCompleted: 25,
    //     setsCompleted: 2,
    //     totalSetsInWorkout: 13,
    //     caloriesBurned: 120
    // }
    
    if (data.currentRep !== undefined && data.totalReps !== undefined) {
        currentRep.textContent = `${data.currentRep}/${data.totalReps}`;
        repProgress.style.width = `${(data.currentRep / data.totalReps) * 100}%`;
    }
    
    if (data.currentSet !== undefined && data.totalSets !== undefined) {
        currentSet.textContent = `${data.currentSet}/${data.totalSets}`;
        setProgress.style.width = `${(data.currentSet / data.totalSets) * 100}%`;
    }
    
    if (data.formScore !== undefined) {
        formScore.textContent = `${data.formScore}%`;
        formProgress.style.width = `${data.formScore}%`;
    }
    
    if (data.totalRepsCompleted !== undefined) {
        totalReps.textContent = data.totalRepsCompleted;
    }
    
    if (data.setsCompleted !== undefined && data.totalSetsInWorkout !== undefined) {
        setsCompleted.textContent = `${data.setsCompleted}/${data.totalSetsInWorkout}`;
    }
    
    if (data.caloriesBurned !== undefined) {
        calories.textContent = data.caloriesBurned;
    }
}

// Set up event listeners
startBtn.addEventListener('click', startWorkout);
pauseBtn.addEventListener('click', pauseWorkout);
stopBtn.addEventListener('click', stopWorkout);

// Initialize the UI when the page loads
document.addEventListener('DOMContentLoaded', initializeUI);

// Example of how to connect with your OpenCV/MediaPipe code
// Replace this with your actual integration code
function setupVideoFeed() {
    // For example, if you're using a canvas to display your video:
    const canvas = document.createElement('canvas');
    canvas.width = 640;
    canvas.height = 360;
    videoFeed.appendChild(canvas);
    
    // Then access the canvas context to draw your video frames
    const ctx = canvas.getContext('2d');
    
    // Your OpenCV/MediaPipe integration code here
    // ...
}

// Call setupVideoFeed to initialize your video stream
// setupVideoFeed();