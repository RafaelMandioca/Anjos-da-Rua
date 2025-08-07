document.addEventListener('DOMContentLoaded', function() {
    // Máscara para campos de Data (DD/MM/AAAA)
    const dateMaskElements = document.querySelectorAll('.date-mask');
    dateMaskElements.forEach(function(element) {
        IMask(element, {
            mask: 'd/m/Y',
            blocks: {
                d: {
                    mask: IMask.MaskedRange,
                    from: 1,
                    to: 31,
                    maxLength: 2,
                },
                m: {
                    mask: IMask.MaskedRange,
                    from: 1,
                    to: 12,
                    maxLength: 2,
                },
                Y: {
                    mask: IMask.MaskedRange,
                    from: 1900,
                    to: new Date().getFullYear() + 10, // Permite datas até 10 anos no futuro
                }
            }
        });
    });

    // Máscara para campos de Data e Hora (DD/MM/AAAA HH:mm)
    const dateTimeMaskElements = document.querySelectorAll('.datetime-mask');
    dateTimeMaskElements.forEach(function(element) {
        IMask(element, {
            mask: 'd/m/Y H:M',
            blocks: {
                d: {
                    mask: IMask.MaskedRange,
                    from: 1,
                    to: 31,
                    maxLength: 2,
                },
                m: {
                    mask: IMask.MaskedRange,
                    from: 1,
                    to: 12,
                    maxLength: 2,
                },
                Y: {
                    mask: IMask.MaskedRange,
                    from: 1900,
                    to: new Date().getFullYear() + 10,
                },
                H: {
                    mask: IMask.MaskedRange,
                    from: 0,
                    to: 23,
                    maxLength: 2,
                },
                M: {
                    mask: IMask.MaskedRange,
                    from: 0,
                    to: 59,
                    maxLength: 2,
                }
            }
        });
    });
});