export class UI {
    constructor(wsClient) {
        this.wsClient = wsClient;
        this.selectedAgents = new Set();
        this.currentQuery = '';
        this.setupEventListeners();
    }

    setupEventListeners() {
        const submitButton = document.getElementById('submitQuery');
        submitButton.addEventListener('click', () => this.handleSubmitQuery());

        const continueButton = document.getElementById('continueWithAgents');
        continueButton.addEventListener('click', () => this.handleContinueWithAgents());
    }

    handleSubmitQuery() {
        const query = document.getElementById('queryInput').value.trim();
        if (!query) return;

        this.currentQuery = query;
        this.selectedAgents.clear();
        this.resetUI();
        this.showProgress('Analyserer spørsmål...');

        this.wsClient.send({ query });
    }

    handleContinueWithAgents() {
        if (this.selectedAgents.size < 2) return;

        this.showProgress('Starter agent-diskusjon...');
        this.wsClient.send({
            type: 'continue_dialogue',
            agents: Array.from(this.selectedAgents),
            query: this.currentQuery
        });
    }

    resetUI() {
        document.getElementById('questionBreakdownContainer').classList.add('hidden');
        document.getElementById('suggestedAgentsContainer').classList.add('hidden');
        document.getElementById('dialogueContainer').innerHTML = '';
    }

    showProgress(message) {
        const progressStatus = document.getElementById('progressStatus');
        const progressText = document.getElementById('progressText');
        progressStatus.classList.remove('hidden');
        progressText.textContent = message;
    }

    hideProgress() {
        document.getElementById('progressStatus').classList.add('hidden');
    }

    displayAgents(agents) {
        const container = document.getElementById('suggestedAgentsContainer');
        const list = document.getElementById('agentList');
        
        list.innerHTML = agents.map(agent => `
            <div class="agent-card bg-white p-4 rounded-lg border">
                <div class="flex items-start space-x-3">
                    <input type="checkbox" value="${agent.role}" class="mt-1">
                    <div>
                        <h3 class="font-medium text-gray-800">${agent.role}</h3>
                        <p class="text-sm text-gray-600 mt-1">${agent.description}</p>
                    </div>
                </div>
            </div>
        `).join('');
        
        container.classList.remove('hidden');
    }

    updateDialogue(dialogueState) {
        const container = document.getElementById('dialogueContainer');
        
        container.innerHTML = dialogueState.map(entry => {
            let headerClass = 'text-gray-700';
            let cardClass = 'bg-white';
            
            if (entry.type === 'consensus') {
                headerClass = 'text-green-700 font-semibold';
                cardClass = 'bg-green-50';
            } else if (entry.type === 'initial-response') {
                cardClass = 'bg-blue-50';
            } else if (entry.type === 'response-to-response') {
                cardClass = 'bg-purple-50';
            }
            
            return `
                <div class="${cardClass} rounded-lg shadow-md p-6 agent-response fade-in">
                    <h3 class="${headerClass} mb-2 text-lg">${entry.agent}</h3>
                    <div class="prose text-gray-600 markdown-content">
                        ${entry.content}
                    </div>
                </div>
            `;
        }).join('');
    }
}
