import React, { useState, useEffect } from "react";
import axios from "axios";

const TableRow = ({ file, token }) => {
	const downloadUrl = `https://controle-documental.onrender.com/arquivos/${file.id}/download/`;

	const downloadFile = async () => {
		try {
			const response = await axios.get(downloadUrl, {
				headers: {
					Accept: "application/json",
					Authorization: `Bearer ${token}`,
					"Content-Type": "multipart/form-data",
				},
			});

			// Cria um link temporário para download do arquivo
			const url = window.URL.createObjectURL(new Blob([response.data]));
			const link = document.createElement("a");
			link.href = url;
			link.setAttribute("download", file.nome);
			document.body.appendChild(link);
			link.click();

			// Libera os recursos
			window.URL.revokeObjectURL(url);
			document.body.removeChild(link);
		} catch (error) {
			console.error("Erro ao baixar arquivo:", error);
		}
	};

	return (
		<tr key={file.id}>
			<td className="px-6 py-4 whitespace-nowrap">
				<div className="flex items-center">
					<div className="ml-4">
						<div className="text-sm font-medium text-gray-900">
							{file.nome}
						</div>
					</div>
				</div>
			</td>
			<td className="px-6 py-4 whitespace-nowrap text-left text-sm font-medium">
				<a
					href={downloadUrl}
					target="_blank"
					rel="noopener noreferrer"
					className="text-indigo-600 hover:text-indigo-900">
					Baixar
				</a>
			</td>
			<td className="px-6 py-4 whitespace-nowrap text-left text-sm font-medium">
				<button onClick={downloadFile}>Baixar </button>
			</td>
		</tr>
	);
};

const TableComponent = () => {
	const [files, setFiles] = useState<any>([]);
	const token =
		"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHJpbmciLCJleHAiOjE3MDM4Njk2MDh9.x48WAz8snLqzoN9cdb6DS51VQxHsIoPnaleYa2HvCZc";

	useEffect(() => {
		const fetchData = async () => {
			try {
				const response = await axios.get(
					"https://controle-documental.onrender.com/arquivos/",
					{
						headers: {
							Authorization: `Bearer ${token}`,
							"Content-Type": "pplication/json",
						},
					}
				);
				setFiles(response.data); // Assumindo que a resposta contém um array de arquivos
			} catch (error) {
				console.error("Erro ao buscar arquivos:", error);
			}
		};

		fetchData();
	}, []);

	return (
		<div className="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8">
			<table className="min-w-full divide-y divide-gray-200">
				<thead className="bg-gray-50">
					<tr>
						<th
							scope="col"
							className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
							Nome do Arquivo PDF
						</th>
						<th
							scope="col"
							className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
							Ação
						</th>
					</tr>
				</thead>
				<tbody className="bg-white divide-y divide-gray-200">
					{files !== null &&
						files.map((file) => (
							<TableRow key={file.id} file={file} token={token} />
						))}
				</tbody>
			</table>
		</div>
	);
};

export default TableComponent;
