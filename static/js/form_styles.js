// static/js/form_styles.js

document.addEventListener('DOMContentLoaded', function() {
    
    function createCustomSelect(selectElement) {
        // Evita recriar o dropdown se o script for executado múltiplas vezes
        if (selectElement.dataset.customized) {
            return;
        }
        selectElement.dataset.customized = 'true';
        selectElement.style.display = 'none';

        const wrapper = document.createElement('div');
        wrapper.className = 'custom-select-wrapper';
        selectElement.parentNode.insertBefore(wrapper, selectElement);
        wrapper.appendChild(selectElement);

        const trigger = document.createElement('div');
        trigger.className = 'custom-select-trigger';
        wrapper.appendChild(trigger);

        const selectedDisplay = document.createElement('span');
        trigger.appendChild(selectedDisplay);
        
        const arrow = document.createElement('span');
        arrow.className = 'custom-arrow';
        trigger.appendChild(arrow);

        const optionsContainer = document.createElement('div');
        optionsContainer.className = 'custom-options';
        wrapper.appendChild(optionsContainer);

        // Popula as opções customizadas e define o texto inicial
        Array.from(selectElement.options).forEach(option => {
            const optionDiv = document.createElement('div');
            optionDiv.className = 'custom-option';
            optionDiv.textContent = option.textContent;
            optionDiv.dataset.value = option.value;
            optionsContainer.appendChild(optionDiv);

            if (option.selected) {
                selectedDisplay.textContent = option.textContent;
                optionDiv.classList.add('selected');
            }

            optionDiv.addEventListener('click', () => {
                // Atualiza o valor do <select> original
                selectElement.value = option.value;
                // Dispara um evento de change para compatibilidade
                selectElement.dispatchEvent(new Event('change'));

                // Atualiza o texto visível
                selectedDisplay.textContent = option.textContent;
                
                // Atualiza a classe 'selected'
                optionsContainer.querySelectorAll('.custom-option').forEach(opt => opt.classList.remove('selected'));
                optionDiv.classList.add('selected');

                // Fecha o dropdown
                wrapper.classList.remove('open');
            });
        });
        
        // Lógica para abrir/fechar e posicionar
        trigger.addEventListener('click', (e) => {
            e.stopPropagation();
            // Fecha outros dropdowns abertos
            document.querySelectorAll('.custom-select-wrapper.open').forEach(openWrapper => {
                if (openWrapper !== wrapper) {
                    openWrapper.classList.remove('open');
                }
            });

            // Lógica de posicionamento (abrir para cima ou para baixo)
            const rect = wrapper.getBoundingClientRect();
            const spaceBelow = window.innerHeight - rect.bottom;
            const optionsHeight = optionsContainer.scrollHeight;

            if (spaceBelow < optionsHeight && rect.top > optionsHeight) {
                optionsContainer.classList.add('open-upward');
            } else {
                optionsContainer.classList.remove('open-upward');
            }

            wrapper.classList.toggle('open');
        });
    }

    // Aplica a customização a todos os selects
    document.querySelectorAll('form select').forEach(createCustomSelect);

    // Fecha o dropdown se clicar fora dele
    window.addEventListener('click', () => {
        document.querySelectorAll('.custom-select-wrapper.open').forEach(wrapper => {
            wrapper.classList.remove('open');
        });
    });
});