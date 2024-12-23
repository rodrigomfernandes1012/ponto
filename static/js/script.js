

// Adiciona o event listener para o botão de processar
document.getElementById('processButton').addEventListener('click', () => {
    // Chama a função para buscar o voucher
    buscarVoucher();
    // Chama o método GET para obter os dados de origem
    fetch('/api/get-origem', {
        method: 'GET'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro ao obter dados de origem');
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            exibirDadosEmTabela(data.dados_viagem, 'tabelaOrigemContainer'); // Passa os dados de origem
             // messageBox.value = data.message;
              //      messageBox.style.display = 'block';
                    document.getElementById('processButton').style.display = 'block';
                    document.getElementById('gerarChamadoButton').style.display = 'block';

        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro na conexão com o servidor.');
    });

    // Chama o método GET para obter os dados de destino
    fetch('/api/get-destino', {
        method: 'GET'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro ao obter dados de destino');
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            exibirDadosEmTabela(data.dados_viagem, 'tabelaDestinoContainer'); // Passa os dados de destino
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro na conexão com o servidor.');
    });
});

// Função para limitar o texto a um número específico de caracteres
function limitarTexto(texto, limite) {
    return texto.length > limite ? texto.substring(0, limite) + '...' : texto;
}

// botao novo
document.getElementById('capture').onclick = async function() {
    // Inicia a contagem regressiva antes de capturar
    let countdown = 1;
    const countdownDisplay = document.getElementById('countdown');

    const countdownInterval = setInterval(() => {
        countdownDisplay.innerText = countdown;
        countdown--;

        if (countdown < 0) {
            clearInterval(countdownInterval);
            capturarTela(); // Chama a função para capturar a tela
        }
    }, 1000);
};

// Função para capturar a tela
async function capturarTela() {
    try {
        const stream = await navigator.mediaDevices.getDisplayMedia({ video: true });
        const video = document.createElement('video');

        video.srcObject = stream;
        video.play();

        // Aguardar um segundo para garantir que a captura esteja pronta
        setTimeout(async () => {
            // Criar um canvas para capturar a imagem
            const canvas = document.createElement('canvas');
            const context = canvas.getContext('2d');

            // Defina a área que deseja capturar
            const x = 10; // Posição x do canto superior esquerdo
            const y = 10; // Posição y do canto superior esquerdo
            const width = 1050; // Largura da área a ser capturada
            const height = 1200; // Altura da área a ser capturada

            const scaleFactor = 1;
            canvas.width = width * scaleFactor;  // Aumenta a largura do canvas
            canvas.height = height * scaleFactor; // Aumenta a altura do canvas

            // Desenhe a parte específica do vídeo no canvas
            context.drawImage(video, x, y, width, height, 0, 0, canvas.width, canvas.height);

            // Para o stream de vídeo
            stream.getTracks().forEach(track => track.stop());

            // Converter o canvas para Data URL
            var dataURL = canvas.toDataURL("image/jpeg");

             // Exibir a imagem capturada na tela
            const imgElement = document.getElementById('capturedImage'); // Elemento onde a imagem será exibida
            imgElement.src = dataURL; // Define o src da imagem como o Data URL


            // Criar um formulário para enviar a imagem
            var data = new FormData();
            data.append('file', dataURLtoBlob(dataURL), 'screenshot.jpeg');

            // Enviar a imagem ao servidor Flask
            fetch('/api/ocr', {
                method: 'POST',
                body: data
            })
            .then(response => response.json())
            .then(result => {
                console.log(result);
                alert("Imagem enviada com sucesso.");

                // Adicionar lógica para preencher campos com os dados retornados, se necessário
                    //messageBox.value = data.message;
                    //messageBox.style.display = 'block';
                    document.getElementById('processButton').style.display = 'block';
                    document.getElementById('gerarChamadoButton').style.display = 'block';
                // Adiciona o event listener para o botão de processar
document.getElementById('processButton').addEventListener('click', () => {
    // Chama a função para buscar o voucher
    buscarVoucher();
    // Chama o método GET para obter os dados de origem
    fetch('/api/get-origem', {
        method: 'GET'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro ao obter dados de origem');
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            exibirDadosEmTabela(data.dados_viagem, 'tabelaOrigemContainer'); // Passa os dados de origem
              //messageBox.value = data.message;
                   // messageBox.style.display = 'block';
                    document.getElementById('processButton').style.display = 'block';
                    document.getElementById('gerarChamadoButton').style.display = 'block';

        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro na conexão com o servidor.');
    });

    // Chama o método GET para obter os dados de destino
    fetch('/api/get-destino', {
        method: 'GET'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro ao obter dados de destino');
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            exibirDadosEmTabela(data.dados_viagem, 'tabelaDestinoContainer'); // Passa os dados de destino
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro na conexão com o servidor.');
    });
});

// Função para limitar o texto a um número específico de caracteres
function limitarTexto(texto, limite) {
    return texto.length > limite ? texto.substring(0, limite) + '...' : texto;
}


                // Fim da logica

            })
            .catch(error => {
                console.error('Erro ao enviar a imagem:', error);
                alert("Houve um erro ao enviar a imagem.");
            });

        }, 1000); // Aguardar 1 segundo para capturar
    } catch (error) {
        console.error('Erro ao capturar a tela:', error);
        alert("Houve um erro ao capturar a tela.");
    }
}

// Função para converter Data URL em Blob
function dataURLtoBlob(dataURL) {
    var arr = dataURL.split(',');
    var mime = arr[0].match(/:(.*?);/)[1];
    var bstr = atob(arr[1]);
    var n = bstr.length;
    var u8arr = new Uint8Array(n);
    while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
    }
    return new Blob([u8arr], { type: mime });
}

// fim do botao novo



// Adiciona o event listener para o botão "Gerar Chamado"
// Adiciona o event listener para o botão "Gerar Chamado"
document.getElementById('gerarChamadoButton').addEventListener('click', () => {
    // Coleta os dados dos campos
    const voucher = document.getElementById('voucher').value;
    const observacao = document.getElementById('observacao').value;
    const origem = document.getElementById('origem').value;
    const destino = document.getElementById('destino').value;
    const valor = document.getElementById('valor').value;
    const viajantes = document.getElementById('viajantes').value;
    const datas = document.getElementById('datas').value;
    const hora = document.getElementById('hora').value;
    const latOrigem = document.getElementById('inputLatOrigem').value;
    const longOrigem = document.getElementById('inputLongOrigem').value;
    const latDestino = document.getElementById('inputLatDestino').value;
    const longDestino = document.getElementById('inputLongDestino').value;
    const telefone = document.getElementById('telefone').value;

    // Valida se todos os campos necessários estão preenchidos
    if (!voucher || !origem || !destino || !valor || !viajantes || !datas || !hora || !latOrigem || !longOrigem || !latDestino || !longDestino) {
        alert('Por favor, preencha todos os campos necessários.');
        return;
    }


    // Envia os dados para o backend através do POST
    fetch('/api/gerar_chamado', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            voucher: voucher,
            observacao: observacao,
            origem: origem,
            telefone: telefone,
            destino: destino,
            valor: valor,
            viajantes: viajantes,
            datas: datas,
            hora: hora,
            inputLatOrigem: latOrigem,
            inputLongOrigem: longOrigem,
            inputLatDestino: latDestino,
            inputLongDestino: longDestino
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro ao gerar o chamado');
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            alert('Erro ao enviar dados: ' + data.error);
        } else {
            alert(data.message || 'Chamado gerado com sucesso!');
            location.reload(); // Recarrega a página após o usuário clicar em OK no alerta
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro na conexão com o servidor ao gerar o chamado.');
    });
});

// Supondo que você tenha uma caixa de texto com id 'origem'
const origemInput = document.getElementById('origem');

// Adiciona o evento de duplo clique na caixa de texto de origem
origemInput.addEventListener('dblclick', () => {
    // Obtém o valor da caixa de texto
    const origem_value = origemInput.value;

    // Envia o valor para o backend através de uma requisição POST
    fetch('/api/get-origem_reload', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ origem: origem_value }) // Envio do valor como JSON
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro ao enviar os dados para o servidor.');
        }
        return response.json();
    })
    .then(data => {
        // Aqui você pode lidar com a resposta do servidor
        console.log('Dados recebidos do servidor:', data);
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro na conexão com o servidor.');
    });
});


// FUNÇÃO PARA EXIBIR OS DADOS DA TABELA

function exibirDadosEmTabela(dadosViagem, containerId, nomeGrupo) {
    const tabelaContainer = document.getElementById(containerId);
    tabelaContainer.innerHTML = ''; // Limpa conteúdo anterior

    const tabela = document.createElement('table');
    tabela.style.width = '80%';
    tabela.style.borderCollapse = 'collapse';

    const cabecalho = tabela.createTHead();
    const linhaCabecalho = cabecalho.insertRow(0);
    const colunas = [ '.', 'Endereço', 'Latitude', 'Longitude'];

    colunas.forEach(coluna => {
        const th = document.createElement('th');
        th.innerText = coluna;
        th.style.border = '1px solid #ddd';
        th.style.padding = '1px';
        th.style.textAlign = 'left';
        linhaCabecalho.appendChild(th);
    });

    const corpoTabela = tabela.createTBody();
    const referenciasVistas = new Set(); // Conjunto para rastrear cdReferencia já vistos

    dadosViagem.forEach(registro => {
        if (!referenciasVistas.has(registro.cdReferencia)) {
            referenciasVistas.add(registro.cdReferencia); // Adiciona a referência ao conjunto para rastreamento

            const novaLinha = corpoTabela.insertRow();
            const celulaSelecionar = novaLinha.insertCell();
            const checkBox = document.createElement('input');

            checkBox.name = nomeGrupo; // Nome diferente por tabela

            const enderecoCelula = novaLinha.insertCell();
            enderecoCelula.innerText = limitarTexto(registro.Endereco, 250); // Limita o Endereço a 250 caracteres
            enderecoCelula.style.border = '1px solid #ddd';
            enderecoCelula.style.padding = '8px';

            const latitudeCelula = novaLinha.insertCell();
            latitudeCelula.innerText = limitarTexto(registro.Latitude, 20); // Limita a Latitude a 20 caracteres
            latitudeCelula.style.border = '1px solid #ddd';
            latitudeCelula.style.padding = '8px';

            const longitudeCelula = novaLinha.insertCell();
            longitudeCelula.innerText = limitarTexto(registro.Longitude, 20); // Limita a Longitude a 20 caracteres
            longitudeCelula.style.border = '1px solid #ddd';
            longitudeCelula.style.padding = '8px';

            // Adiciona o evento de clique duplo à linha
            novaLinha.addEventListener('dblclick', () => {
                if (containerId === 'tabelaOrigemContainer') {
                    // Preenche os campos para a tabela de origem
                    document.getElementById('inputLatOrigem').value = registro.Latitude; // Preenche o campo de latitude
                    document.getElementById('inputLongOrigem').value = registro.Longitude; // Preenche o campo de longitude
                } else if (containerId === 'tabelaDestinoContainer') {
                    // Preenche os campos para a tabela de destino
                    document.getElementById('inputLatDestino').value = registro.Latitude; // Preenche o campo de latitude
                    document.getElementById('inputLongDestino').value = registro.Longitude; // Preenche o campo de longitude
                }
            });
        }
    });

    // Adiciona a tabela ao contêiner especificado
    tabelaContainer.appendChild(tabela);
}
function buscarVoucher() {
    fetch('/api/dados_geral', {
        method: 'GET'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro ao obter dados do voucher');
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            // Assume que o primeiro item do array é o que você precisa
            const dados = data.dados_geral[0]; // Acesse o primeiro elemento do array
            console.log(dados); // Exibe os dados no console

            // Verifica e preenche os campos da UI se os valores forem diferentes
            const voucherField = document.getElementById('voucher');
            const observacaoField = document.getElementById('observacao');
            const origemField = document.getElementById('origem');
            const destinoField = document.getElementById('destino');
            const valorField = document.getElementById('valor');
            const viajantesField = document.getElementById('viajantes');

            if (voucherField.value !== dados.voucher) {
                voucherField.value = dados.voucher || ''; // Preenche o campo se houver valor
            }
            if (observacaoField.value !== dados.observacao) {
                observacaoField.value = dados.observacao || ''; // Preenche o campo se houver observacao
            }
            if (origemField.value !== dados.origem) {
                origemField.value = dados.origem || ''; // Preenche o campo se houver valor
            }
            if (destinoField.value !== dados.destino) {
                destinoField.value = dados.destino || ''; // Preenche o campo se houver valor
            }
            if (valorField.value !== dados.valor) {
                valorField.value = dados.valor || ''; // Preenche o campo se houver valor
            }
            if (viajantesField.value !== dados.viajantes) {
                viajantesField.value = dados.viajantes || ''; // Preenche o campo se houver valor
            }

             if (datas.value !== dados.datas) {
                datas.value = dados.datas || ''; // Preenche o campo se houver valor
            }

              if (hora.value !== dados.hora) {
                hora.value = dados.hora || ''; // Preenche o campo se houver valor
            }
                if (telefone.value !== dados.telefone) {
                telefone.value = dados.telefone || ''; // Preenche o campo se houver valor
            }

        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro na conexão com o servidor.');
    });


}
