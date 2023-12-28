import React, { Fragment, useState } from "react";
import { Disclosure, Menu, Transition } from "@headlessui/react";
import { Bars3Icon, BellIcon, XMarkIcon } from "@heroicons/react/24/outline";
import { FileInput } from "../../components/FileInput";
import * as htmlToImage from "html-to-image";
import axios from "axios";

const user = {
	name: "Tom Cook",
	email: "tom@example.com",
	imageUrl:
		"https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80",
};
const navigation = [
	{ name: "Assinar PDF", href: "#", current: true },
	{ name: "Lista de Documentos Assinados", href: "#", current: false },
];
const userNavigation = [{ name: "Sign out", href: "#" }];

function classNames(...classes) {
	return classes.filter(Boolean).join(" ");
}

function dataURLtoFile(dataURL, fileName) {
	const arr = dataURL.split(",");
	const mime = arr[0].match(/:(.*?);/)[1];
	const bstr = atob(arr[1]);
	let n = bstr.length;
	const u8arr = new Uint8Array(n);

	while (n--) {
		u8arr[n] = bstr.charCodeAt(n);
	}

	return new File([u8arr], fileName, { type: mime });
}

export default function Dashboard() {
	const [file, setFile] = useState<any>();
	const [imageDataUrl, setImageDataUrl] = useState<any>();
	const [signatureName, setSignatureName] = useState("");

	const [assinatura, setAssinatura] = useState<any>();

	const convertTextToImage = async () => {
		try {
			const element = document.getElementById("assinatura");
			if (element !== null) {
				element.style.backgroundColor = "white";
				element.textContent = signatureName;

				htmlToImage
					.toPng(element)
					.then(function (dataUrl) {
						const arquivo = dataURLtoFile(
							dataUrl,
							"assinatura.png"
						);
						setAssinatura(arquivo);
					})
					.catch(function (error) {
						console.error("oops, something went wrong!", error);
					});
			}

			// Define a URL da imagem PNG no estado
		} catch (error) {
			console.error("Oops, algo deu errado!", error);
		}
	};

	const handleFormSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		convertTextToImage();

		const formData = new FormData();
		if (file !== undefined) {
			formData.append("arquivo", file);
		}

		if (assinatura !== undefined) {
			formData.append("assinatura", assinatura);
		}
		formData.append("author", signatureName);

		try {
			// Obtenha o token do local storage
			// const token = localStorage.getItem("token");
			const token =
				"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHJpbmciLCJleHAiOjE3MDM4Njc1NTR9.vXSENvMMCv9vFLbfRj89o5hW5Kz3lSTKdVrWXxbPivg";

			// Realize a requisição POST usando axios
			const response = await axios.post(
				"https://controle-documental.onrender.com/arquivos/",
				formData,
				{
					headers: {
						Accept: "application/json",
						Authorization: `Bearer ${token}`,
						"Content-Type": "multipart/form-data",
					},
				}
			);

			// console.log(response.data);
		} catch (error) {
			console.error("Erro ao enviar a requisição:", error);
		}
	};

	return (
		<>
			<div className="max-h-full">
				<Disclosure as="nav" className="bg-indigo-400">
					{({ open }) => (
						<>
							<div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
								<div className="flex h-16 items-center justify-between">
									<div className="flex items-center">
										<div className="flex-shrink-0">
											<img
												className="h-8 w-8"
												src="/Logo.svg"
												alt="Your Company"
											/>
										</div>
										<div className="hidden md:block">
											<div className="ml-10 flex items-baseline space-x-4">
												{navigation.map((item) => (
													<a
														key={item.name}
														href={item.href}
														className={classNames(
															"text-white hover:bg-gray-700 hover:text-white rounded-md px-3 py-2 text-sm font-medium"
														)}
														aria-current={
															item.current
																? "page"
																: undefined
														}>
														{item.name}
													</a>
												))}
											</div>
										</div>
									</div>
									<div className="hidden md:block">
										<div className="ml-4 flex items-center md:ml-6">
											<button
												type="button"
												className="relative rounded-full bg-gray-800 p-1 text-gray-400 hover:text-white focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800">
												<span className="absolute -inset-1.5" />
												<span className="sr-only">
													View notifications
												</span>
												<BellIcon
													className="h-6 w-6"
													aria-hidden="true"
												/>
											</button>

											{/* Profile dropdown */}
											<Menu
												as="div"
												className="relative ml-3">
												<div>
													<Menu.Button className="relative flex max-w-xs items-center rounded-full bg-gray-800 text-sm focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800">
														<span className="absolute -inset-1.5" />
														<span className="sr-only">
															Open user menu
														</span>
														<img
															className="h-8 w-8 rounded-full"
															src={user.imageUrl}
															alt=""
														/>
													</Menu.Button>
												</div>
												<Transition
													as={Fragment}
													enter="transition ease-out duration-100"
													enterFrom="transform opacity-0 scale-95"
													enterTo="transform opacity-100 scale-100"
													leave="transition ease-in duration-75"
													leaveFrom="transform opacity-100 scale-100"
													leaveTo="transform opacity-0 scale-95">
													<Menu.Items className="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
														{userNavigation.map(
															(item) => (
																<Menu.Item
																	key={
																		item.name
																	}>
																	{({
																		active,
																	}) => (
																		<a
																			href={
																				item.href
																			}
																			className={classNames(
																				active
																					? "bg-gray-100"
																					: "",
																				"block px-4 py-2 text-sm text-gray-700"
																			)}>
																			{
																				item.name
																			}
																		</a>
																	)}
																</Menu.Item>
															)
														)}
													</Menu.Items>
												</Transition>
											</Menu>
										</div>
									</div>
									<div className="-mr-2 flex md:hidden">
										{/* Mobile menu button */}
										<Disclosure.Button className="relative inline-flex items-center justify-center rounded-md bg-gray-800 p-2 text-gray-400 hover:bg-gray-700 hover:text-white focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800">
											<span className="absolute -inset-0.5" />
											<span className="sr-only">
												Open main menu
											</span>
											{open ? (
												<XMarkIcon
													className="block h-6 w-6"
													aria-hidden="true"
												/>
											) : (
												<Bars3Icon
													className="block h-6 w-6"
													aria-hidden="true"
												/>
											)}
										</Disclosure.Button>
									</div>
								</div>
							</div>

							<Disclosure.Panel className="md:hidden">
								<div className="space-y-1 px-2 pb-3 pt-2 sm:px-3">
									{navigation.map((item) => (
										<Disclosure.Button
											key={item.name}
											as="a"
											href={item.href}
											className={classNames(
												item.current
													? "bg-gray-900 text-white"
													: "text-gray-300 hover:bg-gray-700 hover:text-white",
												"block rounded-md px-3 py-2 text-base font-medium"
											)}
											aria-current={
												item.current
													? "page"
													: undefined
											}>
											{item.name}
										</Disclosure.Button>
									))}
								</div>
								<div className="border-t border-gray-700 pb-3 pt-4">
									<div className="flex items-center px-5">
										<div className="flex-shrink-0">
											<img
												className="h-10 w-10 rounded-full"
												src={user.imageUrl}
												alt=""
											/>
										</div>
										<div className="ml-3">
											<div className="text-base font-medium leading-none text-white">
												{user.name}
											</div>
											<div className="text-sm font-medium leading-none text-gray-400">
												{user.email}
											</div>
										</div>
										<button
											type="button"
											className="relative ml-auto flex-shrink-0 rounded-full bg-gray-800 p-1 text-gray-400 hover:text-white focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800">
											<span className="absolute -inset-1.5" />
											<span className="sr-only">
												View notifications
											</span>
											<BellIcon
												className="h-6 w-6"
												aria-hidden="true"
											/>
										</button>
									</div>
									<div className="mt-3 space-y-1 px-2">
										{userNavigation.map((item) => (
											<Disclosure.Button
												key={item.name}
												as="a"
												href={item.href}
												className="block rounded-md px-3 py-2 text-base font-medium text-gray-400 hover:bg-gray-700 hover:text-white">
												{item.name}
											</Disclosure.Button>
										))}
									</div>
								</div>
							</Disclosure.Panel>
						</>
					)}
				</Disclosure>

				<header className="bg-white shadow">
					<div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
						<h1 className="text-3xl font-bold tracking-tight text-gray-900">
							Dashboard
						</h1>
					</div>
				</header>
				<main>
					<div className="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8">
						<FileInput file={file} setFile={setFile} />
					</div>
					{/* <div className="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8">
						<FileInput file={assinatura} setFile={setAssinatura} />
					</div> */}
					<form onSubmit={handleFormSubmit}>
						<div className="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8">
							<label className="block text-sm font-medium leading-6 text-gray-900">
								Informe o nome para assinatura
							</label>
							<div className="mt-2">
								<input
									id="assinatura"
									type="text"
									onChange={(e) =>
										setSignatureName(e.target.value)
									}
									className="block w-full rounded-md border-0 pl-1 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
								/>
							</div>
							<div className="mt-10 flex justify-center items-center">
								<button
									type="submit"
									className="rounded-lg mt-5 bg-indigo-600 px-3.5 py-2.5 text-md w-1/5 font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
									Assinar PDF
								</button>
							</div>
						</div>
					</form>
				</main>
			</div>
		</>
	);
}
