// script.js
document.addEventListener('DOMContentLoaded', () => {
	const content = document.getElementById('content')
	const fileList = document.getElementById('fileList')
	const fileInput = document.getElementById('fileInput')
	let currentFile = null

	const boldButton = document.getElementById('boldButton')
	const italicButton = document.getElementById('italicButton')
	const underlineButton = document.getElementById('underlineButton')
	const strikethroughButton = document.getElementById('strikethroughButton')
	const subscriptButton = document.getElementById('subscriptButton')
	const superscriptButton = document.getElementById('superscriptButton')
	const alignLeftButton = document.getElementById('alignLeftButton')
	const alignCenterButton = document.getElementById('alignCenterButton')
	const alignRightButton = document.getElementById('alignRightButton')
	const alignJustifyButton = document.getElementById('alignJustifyButton')
	const orderedListButton = document.getElementById('orderedListButton')
	const unorderedListButton = document.getElementById('unorderedListButton')
	const headingButton = document.getElementById('headingButton')
	const linkButton = document.getElementById('linkButton')
	const imageButton = document.getElementById('imageButton')
	const tableButton = document.getElementById('tableButton')
	const codeButton = document.getElementById('codeButton')
	const formulaButton = document.getElementById('formulaButton')
	const convertButton = document.getElementById('convertButton')
	const instructionButton = document.getElementById('instructionButton')
	const fontSizeSelect = document.getElementById('fontSizeSelect')
	const fontFamilySelect = document.getElementById('fontFamilySelect')

	// Handle file input change
	fileInput.addEventListener('change', async () => {
		const formData = new FormData()
		formData.append('file', fileInput.files[0])

		try {
			const response = await fetch('http://skyrodev.ru:8000/api/v1/latex/upload', {
				method: 'POST',
				body: formData,
			})
			if (!response.ok) {
				throw new Error(`HTTP ошибка! статус: ${response.status}`)
			}
			const result = await response.json()
			if (result.статус === 'успех') {
				alert('Файл успешно загружен!')
				loadFiles()
				fileInput.value = '' // Очистить поле ввода файла
			} else {
				alert(`Ошибка: ${result.детали}`)
			}
		} catch (error) {
			alert(`Ошибка: ${error.message}`)
		}
	})

	// Load available files
	const loadFiles = async () => {
		try {
			const response = await fetch('http://skyrodev.ru:8000/api/v1/latex/get-all-files')
			if (!response.ok) {
				throw new Error(`HTTP ошибка! статус: ${response.status}`)
			}
			const result = await response.json()
			fileList.innerHTML = ''
			result.forEach(file => {
				const fileName = file.replace(/\.[^/.]+$/, '') // Удаление расширения
				const li = document.createElement('li')
				li.innerHTML = `
                    <span>${file}</span>
                    <button class="delete-button" onclick="deleteFile('${fileName}')">
                        <img src="/static/photo/trash.svg" alt="Удалить">
                    </button>
                `
				li.addEventListener('click', () => {
					currentFile = fileName
					loadFileContent(file)
				})
				fileList.appendChild(li)
			})
		} catch (error) {
			console.error('Ошибка загрузки файлов:', error)
		}
	}

	// Load content of a specific file
	const loadFileContent = async fileName => {
		try {
			const response = await fetch(
				`http://skyrodev.ru:8000/api/v1/latex/get-latex?file_name=${fileName}`
			)
			if (!response.ok) {
				throw new Error(`HTTP ошибка! статус: ${response.status}`)
			}
			const result = await response.json()
			content.innerHTML = result.латекс_контент
		} catch (error) {
			console.error('Ошибка загрузки содержимого файла:', error)
		}
	}

	// Save content to the current file
	window.saveContent = async () => {
		if (!currentFile) {
			alert('Пожалуйста, выберите файл для сохранения.')
			return
		}
		try {
			const response = await fetch(`http://skyrodev.ru:8000/api/v1/latex/update-latex`, {
				method: 'PUT',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({
					file_name: currentFile,
					latex_content: content.innerHTML,
				}),
			})
			if (!response.ok) {
				throw new Error(`HTTP ошибка! статус: ${response.status}`)
			}
			const result = await response.json()
			alert(result.детали)
		} catch (error) {
			console.error('Ошибка сохранения содержимого файла:', error)
		}
	}

	// Text formatting functions
	window.toggleBold = () => {
		document.execCommand('bold', false, null)
		boldButton.classList.toggle('active')
	}

	window.toggleItalic = () => {
		document.execCommand('italic', false, null)
		italicButton.classList.toggle('active')
	}

	window.toggleUnderline = () => {
		document.execCommand('underline', false, null)
		underlineButton.classList.toggle('active')
	}

	window.toggleStrikethrough = () => {
		document.execCommand('strikethrough', false, null)
		strikethroughButton.classList.toggle('active')
	}

	window.toggleSubscript = () => {
		document.execCommand('subscript', false, null)
		subscriptButton.classList.toggle('active')
	}

	window.toggleSuperscript = () => {
		document.execCommand('superscript', false, null)
		superscriptButton.classList.toggle('active')
	}

	window.alignLeft = () => {
		document.execCommand('justifyLeft', false, null)
		alignLeftButton.classList.toggle('active')
		alignCenterButton.classList.remove('active')
		alignRightButton.classList.remove('active')
		alignJustifyButton.classList.remove('active')
	}

	window.alignCenter = () => {
		document.execCommand('justifyCenter', false, null)
		alignCenterButton.classList.toggle('active')
		alignLeftButton.classList.remove('active')
		alignRightButton.classList.remove('active')
		alignJustifyButton.classList.remove('active')
	}

	window.alignRight = () => {
		document.execCommand('justifyRight', false, null)
		alignRightButton.classList.toggle('active')
		alignLeftButton.classList.remove('active')
		alignCenterButton.classList.remove('active')
		alignJustifyButton.classList.remove('active')
	}

	window.alignJustify = () => {
		document.execCommand('justifyFull', false, null)
		alignJustifyButton.classList.toggle('active')
		alignLeftButton.classList.remove('active')
		alignCenterButton.classList.remove('active')
		alignRightButton.classList.remove('active')
	}

	window.createOrderedList = () => {
		document.execCommand('insertOrderedList', false, null)
	}

	window.createUnorderedList = () => {
		document.execCommand('insertUnorderedList', false, null)
	}

	window.createHeading = () => {
		document.execCommand('formatBlock', false, '<h1>')
	}

	window.createLink = () => {
		const url = prompt('Введите URL:')
		if (url) {
			document.execCommand('createLink', false, url)
		}
	}

	window.insertImage = () => {
		const imageUrl = prompt('Введите URL изображения:')
		if (imageUrl) {
			const img = document.createElement('img')
			img.src = imageUrl
			img.style.maxWidth = '100%'
			img.style.height = 'auto'
			img.contentEditable = 'true'
			content.appendChild(img)
		}
	}

	window.createTable = () => {
		const rows = prompt('Введите количество строк:')
		const cols = prompt('Введите количество столбцов:')
		if (rows && cols) {
			let tableHTML = '<table border="1">'
			for (let i = 0; i < parseInt(rows); i++) {
				tableHTML += '<tr>'
				for (let j = 0; j < parseInt(cols); j++) {
					tableHTML += '<td contenteditable="true"></td>'
				}
				tableHTML += '</tr>'
			}
			tableHTML += '</table>'
			content.innerHTML += tableHTML
		}
	}

	window.insertCode = () => {
		const code = prompt('Введите код:')
		if (code) {
			const pre = document.createElement('pre')
			pre.textContent = code
			content.appendChild(pre)
		}
	}

	window.openFormulaPage = () => {
		window.open('http://skyrodev.ru:8000/formula', '_blank')
	}

	window.openConvertPage = () => {
		window.open('http://skyrodev.ru:8000/convert', '_blank')
	}

	window.openInstructionPage = () => {
		window.open('http://skyrodev.ru:8000/instruction', '_blank')
	}

	window.changeFontSize = () => {
		const fontSize = fontSizeSelect.value
		document.execCommand('fontSize', false, fontSize)
	}

	window.changeFontFamily = () => {
		const fontFamily = fontFamilySelect.value
		document.execCommand('fontName', false, fontFamily)
	}

	// Delete a specific file
	window.deleteFile = async fileName => {
		try {
			const response = await fetch(
				`http://skyrodev.ru:8000/api/v1/latex/delete-file?file_name=${fileName}`,
				{
					method: 'DELETE',
				}
			)
			if (!response.ok) {
				throw new Error(`HTTP ошибка! статус: ${response.status}`)
			}
			const result = await response.json()
			alert(result.детали)
			loadFiles() // Перезагрузить список файлов
		} catch (error) {
			console.error('Ошибка удаления файла:', error)
		}
	}

	// Initial load of files
	loadFiles()
})
