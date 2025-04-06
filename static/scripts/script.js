// Function to switch between tabs
function switchTab(tabName) {
    const contents = document.querySelectorAll('.tab-content');
    contents.forEach(content => content.classList.remove('active'));

    const tabs = document.querySelectorAll('.tabs div');
    tabs.forEach(tab => tab.classList.remove('active'));

    document.getElementById(tabName).classList.add('active');
    document.getElementById(tabName + '-tab').classList.add('active');
}

// Function to toggle the visibility of the answer
function toggleAnswer(index) {
    var answerDiv = document.getElementById("answer-" + index);
    answerDiv.classList.toggle("hidden");
}

// Function to handle the Home button click
function goHome() {
    // Clear the question history
    history = [];

    // Clear the answers in the sidebar
    const answerDivs = document.querySelectorAll('.hidden');
    answerDivs.forEach(answer => answer.classList.remove('hidden'));

    // Optionally, reset the form inputs (if any)
    document.querySelectorAll('input[type="text"]').forEach(input => {
        input.value = ''; // Clear text inputs
    });

    // Set the active tab back to 'Ask Question' tab
    document.getElementById('ask-question').classList.add('active');
    document.getElementById('articles').classList.remove('active');

    // Optionally reset any specific UI changes like removing answers from view
    const answers = document.querySelectorAll('.answer');
    answers.forEach(answer => answer.style.display = 'none');

    // Reset articles section if needed
    document.querySelector('.article-list').innerHTML = '';
}
