document.addEventListener("DOMContentLoaded", () => {
    const chatForm = document.getElementById('chatForm');
    const userInput = document.getElementById('userInput');
    const chatContainer = document.getElementById('chatContainer');
    const sendBtn = document.getElementById('sendBtn');
    const modelStatus = document.getElementById('modelStatus');
    const iterationCount = document.getElementById('iterationCount');
    const iterBar = document.getElementById('iterBar');

    let msgCount = 0;

    function appendMessage(role, content) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${role}-msg`;

        const contentDiv = document.createElement('div');
        contentDiv.className = 'msg-content';
        contentDiv.textContent = content;

        msgDiv.appendChild(contentDiv);
        chatContainer.appendChild(msgDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    function showTyping() {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message agent-msg';
        msgDiv.id = 'typingIndicator';

        const contentDiv = document.createElement('div');
        contentDiv.className = 'msg-content typing-indicator';

        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('div');
            dot.className = 'typing-dot';
            contentDiv.appendChild(dot);
        }

        msgDiv.appendChild(contentDiv);
        chatContainer.appendChild(msgDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    function removeTyping() {
        const indicator = document.getElementById('typingIndicator');
        if (indicator) indicator.remove();
    }

    function updateMetrics(state) {
        if (state === 'thinking') {
            modelStatus.textContent = 'PROCESSING';
            modelStatus.className = 'metric-value accent-secondary';
            // Simulate iteration progress
            msgCount++;
            const iters = Math.min(msgCount, 15);
            iterationCount.textContent = `${iters} / 15`;
            iterBar.style.width = `${(iters / 15) * 100}%`;

            // Update thread status
            const threadItems = document.querySelectorAll('.thread-item .status-active');
            threadItems.forEach(el => {
                el.textContent = 'RUNNING';
                el.style.color = 'var(--secondary-fixed-dim)';
            });
        } else {
            modelStatus.textContent = 'READY';
            modelStatus.className = 'metric-value accent-primary-bright';

            const threadItems = document.querySelectorAll('.thread-item .status-active');
            threadItems.forEach(el => {
                el.textContent = 'IDLE';
                el.style.color = '';
            });
        }
    }

    // Tool button clicks insert tool name into input
    document.querySelectorAll('.tool-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const tool = btn.getAttribute('data-tool');
            userInput.value = `Use the ${tool} tool to `;
            userInput.focus();
        });
    });

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const text = userInput.value.trim();
        if (!text) return;

        appendMessage('user', text);
        userInput.value = '';
        sendBtn.disabled = true;
        showTyping();
        updateMetrics('thinking');

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });

            if (!response.ok) throw new Error("Network response was not ok");

            const data = await response.json();
            removeTyping();
            appendMessage('agent', data.response);
        } catch (error) {
            console.error('Error:', error);
            removeTyping();
            appendMessage('agent', '[ERROR] Connection to agent backend failed. Make sure the server is running.');
        } finally {
            sendBtn.disabled = false;
            updateMetrics('ready');
            userInput.focus();
        }
    });

    // ==========================================
    // TAB SWITCHING LOGIC
    // ==========================================
    const navLinks = document.querySelectorAll('.nav-link, .mobile-link');
    const tabContents = document.querySelectorAll('.tab-content');

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetTab = link.getAttribute('data-tab');
            if (!targetTab) return;

            // Update active link state
            navLinks.forEach(nav => nav.classList.remove('active'));
            document.querySelectorAll(`[data-tab="${targetTab}"]`).forEach(nav => nav.classList.add('active'));

            // Update active tab content
            tabContents.forEach(tab => {
                if (tab.id === `tab-${targetTab}`) {
                    tab.classList.add('active');
                } else {
                    tab.classList.remove('active');
                }
            });
        });
    });

    // ==========================================
    // SSE LOG STREAMING (TERMINAL)
    // ==========================================
    const terminalOutput = document.getElementById('terminalOutput');
    
    function appendTerminalLine(text, className = '') {
        const div = document.createElement('div');
        div.className = `term-line ${className}`;
        div.textContent = text;
        terminalOutput.appendChild(div);
        terminalOutput.scrollTop = terminalOutput.scrollHeight;
    }

    try {
        const eventSource = new EventSource("/api/stream");
        
        eventSource.onmessage = function(event) {
            const data = JSON.parse(event.data);
            
            if (data.type === "llm_start") {
                appendTerminalLine(`[*] ${data.content}`, "sys-msg");
            } else if (data.type === "tool_start") {
                appendTerminalLine(`[EXEC] Calling ${data.tool} with input: ${data.input}`, "tool-exec");
                // Update metrics panel activity
                document.querySelectorAll('.node-item').forEach(el => el.classList.remove('active-tool'));
                const toolNodes = document.querySelectorAll('.node-item .node-name');
                toolNodes.forEach(node => {
                    if (data.tool.toLowerCase().includes(node.textContent.toLowerCase())) {
                        node.closest('.node-item').classList.add('active-tool');
                    }
                });
            } else if (data.type === "tool_end") {
                appendTerminalLine(`[RES] ${data.output}`, "tool-out");
            } else if (data.type === "agent_action") {
                if (data.log) {
                    const thought = data.log.split('Action:')[0].trim();
                    if (thought) appendTerminalLine(`[THINK] ${thought}`, "agent-thought");
                }
            } else if (data.type === "agent_finish") {
                appendTerminalLine(`[+] AGENT TASK COMPLETED`, "sys-msg");
                document.querySelectorAll('.node-item').forEach(el => el.classList.remove('active-tool'));
            }
        };

        eventSource.onerror = function(err) {
            console.error("EventSource failed:", err);
            appendTerminalLine("[!] Connection to event stream lost. Retrying...", "sys-msg");
        };
    } catch (e) {
        console.error("SSE Error:", e);
    }
});
