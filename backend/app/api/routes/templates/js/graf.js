function plotGraph() {
	// Получаем выражение
	const expression = document.getElementById('expression').value
	if (!expression) {
		alert('Пожалуйста, введите выражение для графика.')
		return
	}

	// Диапазоны для x и y
	const xRange = [-2, 2]
	const yRange = [-2, 2]
	const xStep = 0.1
	const yStep = 0.1

	// Массивы для хранения точек графика
	const xValues = []
	const yValues = []
	const zValues = []

	// Процесс создания точек для графика
	for (let x = xRange[0]; x <= xRange[1]; x += xStep) {
		for (let y = yRange[0]; y <= yRange[1]; y += yStep) {
			try {
				// Вычисляем значение z для каждой точки (x, y)
				const z = math.evaluate(expression, { x: x, y: y })
				if (isFinite(z)) {
					// Проверка на конечность значения z
					xValues.push(x)
					yValues.push(y)
					zValues.push(z)
				}
			} catch (e) {
				// Ошибка вычисления — пропускаем эту точку
				console.error('Ошибка вычисления для x: ' + x + ', y: ' + y, e)
			}
		}
	}

	if (xValues.length === 0) {
		alert('Не удалось построить график. Проверьте ваше выражение.')
		return
	}

	// Данные для графика
	const trace = {
		x: xValues,
		y: yValues,
		z: zValues,
		type: 'scatter3d',
		mode: 'markers',
		marker: {
			size: 3,
			color: zValues,
			colorscale: 'Viridis',
			opacity: 0.7,
		},
	}

	const layout = {
		scene: {
			xaxis: { title: 'X' },
			yaxis: { title: 'Y' },
			zaxis: { title: 'Z' },
		},
		title: '3D график: ' + expression,
	}

	// Рисуем график с помощью Plotly
	Plotly.newPlot('graph', [trace], layout)
}

function insertLatex() {
	// Вставить выражение в LaTeX формат
	const expression = document.getElementById('expression').value
	if (expression) {
		document.getElementById('latexInput').value = `\\(${expression}\\)`
	}
}
