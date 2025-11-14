function showTab(tabName) {
    const tabs = document.querySelectorAll('.tab');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabs.forEach(tab => tab.classList.remove('active'));
    tabContents.forEach(content => content.classList.remove('active'));
    
    const selectedTab = Array.from(tabs).find(tab => 
        tab.textContent.toLowerCase().includes(tabName.toLowerCase()) ||
        tab.onclick.toString().includes(tabName)
    );
    
    if (selectedTab) {
        selectedTab.classList.add('active');
    }
    
    const targetContent = document.getElementById(tabName + '-tab');
    if (targetContent) {
        targetContent.classList.add('active');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const today = new Date().toISOString().split('T')[0];
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        input.max = today;
        if (!input.value) {
            input.value = today;
        }
    });
});
