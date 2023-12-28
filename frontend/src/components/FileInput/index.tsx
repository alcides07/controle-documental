import React from "react";

import { useCallback, useState } from "react";
import { DropzoneState, useDropzone } from "react-dropzone";
import { CloseIcon } from "../icons/CloseIcon";
import { FileIcon } from "../icons/FileIcon";
import { UploadIcon } from "../icons/UploadIcon";

interface InputProps {
	dropzone: DropzoneState;
}

interface HasFileProps {
	file?: File;
	removeFile: () => void;
}

export const FileInput = ({ file, setFile }) => {
	const removeFile = useCallback(() => {
		setFile(null);
	}, [file]);

	const onDrop = useCallback((files: File[]) => {
		setFile(files[0]);
	}, []);

	const dropzone = useDropzone({
		onDrop,
		accept: {
			"image/png": [".png"],
			"application/pdf": [".pdf"],
		},
	});

	if (file) return <HasFile file={file} removeFile={removeFile} />;

	return <Input dropzone={dropzone} />;
};

const Input = ({ dropzone }: InputProps) => {
	const { getRootProps, getInputProps, isDragActive } = dropzone;

	return (
		<div
			{...getRootProps()}
			className={`w-full h-full rounded-lg border-dashed border-4 hover:border-indigo-900 bg-indigo-300 hover:bg-indigo-400 transition-all
      ${isDragActive ? "border-blue-500" : "border-indigo-500"}`}>
			<label
				htmlFor="dropzone-file"
				className="cursor-pointer w-full h-full">
				<div className="flex flex-col items-center justify-center pt-5 pb-6 w-full h-full">
					<UploadIcon
						className={`w-10 h-10 mb-3 text-gray-950 ${
							isDragActive ? "text-blue-500" : "text-gray-400"
						}`}
					/>
					{isDragActive ? (
						<p className="font-bold text-lg text-gray-950">
							Solte para adicionar
						</p>
					) : (
						<>
							<p className="mb-2 text-lg text-gray-950">
								<span className="font-bold ">
									Clique para enviar
								</span>{" "}
								ou arraste até aqui
							</p>
							<p className="text-gray-950 text-sm">PDF</p>
						</>
					)}
				</div>
			</label>
			<input {...getInputProps()} className="hidden" />
		</div>
	);
};

const HasFile = ({ file, removeFile }: HasFileProps) => {
	return (
		<div className="w-full h-full rounded-lg border-dashed border-4 hover:border-indigo-900 bg-indigo-300 hover:bg-indigo-400 transition-all">
			<div className="bg-white w-50 rounded-md shadow-md flex gap-3 items-center justify-center">
				<FileIcon className="w-5 h-12 my-12 ml-4" />
				<span className="text-sm text-gray-500 my-4">{file?.name}</span>
				<button
					type="button"
					onClick={removeFile}
					className="place-self-start mt-1 p-1">
					<CloseIcon className="w-5 h-5" />
				</button>
			</div>
		</div>
	);
};
