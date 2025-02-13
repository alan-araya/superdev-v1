let currentData = [];

function createSeatElement(seat, isFree) {
    const seatDiv = document.createElement('div');
    seatDiv.className = `seat seat-${seat.seat_type.toLowerCase().replace(' ', '-')}${!isFree ? ' seat-occupied' : ''}`;
    seatDiv.textContent = seat.seat.replace(/[0-9]/g, '');
    return seatDiv;
}
function renderSeats(seats) {
    const container = document.getElementById('seatContainer');
    container.innerHTML = '';

    // Ordenar assentos numericamente
    const sortedSeats = seats.sort((a, b) => {
        const aRow = parseInt(a.seat.match(/^\d+/)[0]);
        const bRow = parseInt(b.seat.match(/^\d+/)[0]);
        const aLetter = a.seat.match(/[A-Za-z]+/)[0];
        const bLetter = b.seat.match(/[A-Za-z]+/)[0];
        return aRow - bRow || aLetter.localeCompare(bLetter);
    });

    // Agrupar por fileira
    const rows = Array.from({length: 34}, (_, i) => i + 1);

    rows.forEach(rowNumber => {
        const rowSeats = sortedSeats.filter(s => 
            parseInt(s.seat.match(/^\d+/)[0]) === rowNumber
        );
        const seatType = rowSeats[0]?.seat_type;

        const rowDiv = document.createElement('div');
        rowDiv.className = 'row';

        // Número da fileira
        const rowNumberDiv = document.createElement('div');
        rowNumberDiv.className = 'row-number';
        rowNumberDiv.textContent = rowNumber;

        // Grupos de assentos
        const leftGroup = document.createElement('div');
        leftGroup.className = 'seat-group';
        
        const rightGroup = document.createElement('div');
        rightGroup.className = 'seat-group';

        // Lógica Economy Premium
        if (seatType === 'Economy Premium') {
            // Esquerda: A, B + inválido
            ['A', 'B'].forEach(letter => {
                const seat = rowSeats.find(s => s.seat.endsWith(letter));
                leftGroup.appendChild(createSeatElement(seat, seat?.is_free));
            });
            leftGroup.appendChild(createInvalidSeat());

            // Direita: C, D + inválido
            ['C', 'D'].forEach(letter => {
                const seat = rowSeats.find(s => s.seat.endsWith(letter));
                rightGroup.appendChild(createSeatElement(seat, seat?.is_free));
            });
            rightGroup.appendChild(createInvalidSeat());
        } else {
            // Demais classes
            ['A', 'B', 'C'].forEach(letter => {
                const seat = rowSeats.find(s => s.seat.endsWith(letter));
                if (seat) leftGroup.appendChild(createSeatElement(seat, seat.is_free));
            });
            
            ['D', 'E', 'F'].forEach(letter => {
                const seat = rowSeats.find(s => s.seat.endsWith(letter));
                if (seat) rightGroup.appendChild(createSeatElement(seat, seat.is_free));
            });
        }

        rowDiv.appendChild(rowNumberDiv);
        rowDiv.appendChild(leftGroup);
        rowDiv.appendChild(rightGroup);
        container.appendChild(rowDiv);
    });
}

function createInvalidSeat() {
    const invalidSeat = document.createElement('div');
    invalidSeat.className = 'seat seat-invalid';
    invalidSeat.textContent = '';
    return invalidSeat;
}

async function fetchSeats() {
    try {
        const response = await fetch('http://127.0.0.1:5000/flight/seats');
        const data = await response.json();
        if (JSON.stringify(data) !== JSON.stringify(currentData)) {
            currentData = data;
            renderSeats(data);
        }
    } catch (error) {
        console.error('Erro ao carregar assentos:', error);
    }
}

// Atualização automática a cada 1 segundo
setInterval(fetchSeats, 1000);

// Carregamento inicial
window.onload = fetchSeats;