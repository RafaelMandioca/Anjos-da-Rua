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
        
        const searchInput = document.createElement('input');
        searchInput.type = 'text';
        searchInput.className = 'custom-select-search';
        const label = document.querySelector(`label[for="${selectElement.id}"]`);
        searchInput.placeholder = `Buscar ${label ? label.textContent.toLowerCase() : 'opção'}...`;
        trigger.appendChild(searchInput);

        if (selectElement.disabled) {
            wrapper.classList.add('is-disabled');
            searchInput.disabled = true;
        }

        const arrow = document.createElement('span');
        arrow.className = 'custom-arrow';
        trigger.appendChild(arrow);

        const optionsContainer = document.createElement('div');
        optionsContainer.className = 'custom-options';
        wrapper.appendChild(optionsContainer);

        Array.from(selectElement.options).forEach(option => {
            const optionDiv = document.createElement('div');
            optionDiv.className = 'custom-option';
            optionDiv.textContent = option.textContent;
            optionDiv.dataset.value = option.value;
            optionsContainer.appendChild(optionDiv);

            if (option.selected && option.value) {
                searchInput.value = option.textContent;
                optionDiv.classList.add('selected');
            }

            optionDiv.addEventListener('click', (e) => {
                e.stopPropagation();
                selectElement.value = option.value;
                selectElement.dispatchEvent(new Event('change'));

                searchInput.value = option.textContent;
                
                optionsContainer.querySelectorAll('.custom-option').forEach(opt => opt.classList.remove('selected'));
                optionDiv.classList.add('selected');

                wrapper.classList.remove('open');
                optionsContainer.querySelectorAll('.custom-option').forEach(opt => {
                    opt.style.display = '';
                });
            });
        });

        searchInput.addEventListener('input', () => {
            const filter = searchInput.value.toLowerCase();
            optionsContainer.querySelectorAll('.custom-option').forEach(opt => {
                const text = opt.textContent.toLowerCase();
                opt.style.display = text.includes(filter) ? '' : 'none';
            });
            if (!wrapper.classList.contains('open')) {
                wrapper.classList.add('open');
            }
        });

        searchInput.addEventListener('blur', () => {
            setTimeout(() => {
                const selectedOption = selectElement.options[selectElement.selectedIndex];
                if (searchInput.value !== selectedOption.textContent) {
                    searchInput.value = selectedOption.textContent;
                }
            }, 150);
        });
        
        trigger.addEventListener('click', (e) => {
            if (wrapper.classList.contains('is-disabled')) return;
            e.stopPropagation();

            document.querySelectorAll('.custom-select-wrapper.open').forEach(openWrapper => {
                if (openWrapper !== wrapper) {
                    openWrapper.classList.remove('open');
                }
            });

            const rect = wrapper.getBoundingClientRect();
            const spaceBelow = window.innerHeight - rect.bottom;
            const optionsHeight = optionsContainer.scrollHeight;

            if (spaceBelow < optionsHeight && rect.top > optionsHeight) {
                optionsContainer.classList.add('open-upward');
            } else {
                optionsContainer.classList.remove('open-upward');
            }

            wrapper.classList.toggle('open');
            if (wrapper.classList.contains('open')) {
                searchInput.focus();
                searchInput.select();
            }
        });

        searchInput.addEventListener('click', (e) => {
            e.stopPropagation();
        });
    }

    document.querySelectorAll('form select').forEach(createCustomSelect);

    window.addEventListener('click', () => {
        document.querySelectorAll('.custom-select-wrapper.open').forEach(wrapper => {
            wrapper.classList.remove('open');
            
            const select = wrapper.querySelector('select');
            const search = wrapper.querySelector('.custom-select-search');
            if (select && search) {
                const selectedOption = select.options[select.selectedIndex];
                if (selectedOption) {
                    search.value = selectedOption.textContent;
                }
            }
        });
    });
});