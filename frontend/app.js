document.addEventListener("DOMContentLoaded", function () {
    const seatContainer = document.getElementById("seat-container");

    // Função para carregar os dados de assentos da API
    async function loadSeats() {
        try {
            const response = await fetch('http://127.0.0.1:5000/flight/seats');
            const seats = await response.json();
            renderSeats(seats);
        } catch (error) {
            console.error("Erro ao carregar os assentos:", error);
        }
    }

    // Função para adicionar assentos vazios para manter o alinhamento
    function addEmptySeats(group, count) {
        for (let i = 0; i < count; i++) {
            const emptySeat = document.createElement("div");
            emptySeat.classList.add("seat", "empty");
            group.appendChild(emptySeat);
        }
    }

    // Função para renderizar os assentos
    function renderSeats(seats) {
        seatContainer.innerHTML = ""; // Limpa o container antes de adicionar os assentos

        let currentRow = '';
        let rowElement = null;
        let leftGroup = null;
        let rightGroup = null;

        seats.forEach((seat, index) => {
            // Extrair o número da fileira usando uma regex que pega apenas os dígitos
            const seatRowNumber = seat.seat.match(/\d+/)[0];

            if (seatRowNumber !== currentRow) {
                // Se for uma nova fileira, inicializa a nova linha e os grupos
                currentRow = seatRowNumber;
                rowElement = document.createElement("div");
                rowElement.classList.add("row");

                const rowNumber = document.createElement("div");
                rowNumber.classList.add("row-number");
                rowNumber.textContent = currentRow;

                rowElement.appendChild(rowNumber);

                leftGroup = document.createElement("div");
                leftGroup.classList.add("seat-group", "seat-group-left");

                rightGroup = document.createElement("div");
                rightGroup.classList.add("seat-group", "seat-group-right");

                rowElement.appendChild(leftGroup);
                rowElement.appendChild(rightGroup);
                seatContainer.appendChild(rowElement);
            }

            const seatElement = document.createElement("div");
            seatElement.classList.add("seat");

            // Definindo a cor conforme o tipo e ocupação do assento
            if (!seat.is_free) {
                seatElement.classList.add("occupied");
            } else {
                switch (seat.seat_type) {
                    case "Premium":
                        seatElement.classList.add("premium");
                        break;
                    case "Economy Premium":
                        seatElement.classList.add("economy-premium");
                        break;
                    case "Economy":
                        seatElement.classList.add("economy");
                        break;
                }
            }

            seatElement.textContent = seat.seat;

            // Adiciona o assento no grupo correto
            if(seat.seat_type === "Economy Premium") {
                if (["A", "B"].includes(seat.seat.slice(-1))) {
                    leftGroup.appendChild(seatElement);
                } else if (["C", "D"].includes(seat.seat.slice(-1))) {
                    rightGroup.appendChild(seatElement);
                }
            } else  
            {                
                if (["A", "B", "C"].includes(seat.seat.slice(-1))) {
                    leftGroup.appendChild(seatElement);
                } else if (["D", "E", "F"].includes(seat.seat.slice(-1))) {
                    rightGroup.appendChild(seatElement);
                }
            }
        

            // Verificar se é a última fileira e ajustar o alinhamento de "Economy Premium"
            if ((index === seats.length - 1 || seats[index + 1].seat.match(/\d+/)[0] !== currentRow) &&
                seat.seat_type === "Economy Premium") {
                // Adiciona assentos vazios para alinhar a fileira
                addEmptySeats(leftGroup, 3 - leftGroup.children.length); // Preencher o grupo esquerdo se faltarem assentos
                addEmptySeats(rightGroup, 3 - rightGroup.children.length); // Preencher o grupo direito se faltarem assentos
            }
        });
    }

    // Carregar os assentos ao iniciar a tela
    loadSeats();
});
