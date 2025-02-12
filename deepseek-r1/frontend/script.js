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

    const rows = Array.from({length: 34}, (_, i) => i + 1);
    
    rows.forEach(rowNumber => {
        const rowDiv = document.createElement('div');
        rowDiv.className = 'row';
        
        const rowNumberDiv = document.createElement('div');
        rowNumberDiv.className = 'row-number';
        rowNumberDiv.textContent = rowNumber;
        
        const leftGroup = document.createElement('div');
        leftGroup.className = 'seat-group';
        
        const rightGroup = document.createElement('div');
        rightGroup.className = 'seat-group';

        const rowSeats = seats.filter(s => parseInt(s.seat) === rowNumber);
        const seatType = rowSeats[0]?.seat_type;

        // Lado Esquerdo (A,B,C)
        ['A', 'B', 'C'].forEach(letter => {
            const seat = rowSeats.find(s => s.seat.endsWith(letter));
            if (seat) {
                leftGroup.appendChild(createSeatElement(seat, seat.is_free));
            } else if (seatType === 'Economy Premium' && letter === 'C') {
                leftGroup.appendChild(createInvalidSeat());
            }
        });

        // Lado Direito (D,E,F)
        ['D', 'E', 'F'].forEach(letter => {
            const seat = rowSeats.find(s => s.seat.endsWith(letter));
            if (seat) {
                rightGroup.appendChild(createSeatElement(seat, seat.is_free));
            } else if (seatType === 'Economy Premium' && letter === 'E') {
                rightGroup.appendChild(createInvalidSeat());
            }
        });

        rowDiv.appendChild(rowNumberDiv);
        rowDiv.appendChild(leftGroup);
        rowDiv.appendChild(document.createTextNode(' ')); // Espaço entre grupos
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