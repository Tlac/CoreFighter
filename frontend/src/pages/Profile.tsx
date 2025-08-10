import {useQuery} from "@tanstack/react-query"
import {api} from "@/api/client"
import {Link} from "react-router-dom"
import {Deck} from "@/types";

export default function Profile() {
    const {data, isLoading, isError, error, refetch} = useQuery({
        queryKey: ["my-decks"],
        queryFn: () => api<Deck[]>("/api/decks/"),
    })

    if (isLoading) {
        return (
            <div className="p-6">
                <h1 className="text-2xl font-bold">My Decks</h1>
                <p className="mt-3 text-slate-600">Loading your decks…</p>
            </div>
        )
    }

    if (isError) {
        return (
            <div className="p-6">
                <h1 className="text-2xl font-bold">My Decks</h1>
                <div className="mt-3 rounded-md border border-red-200 bg-red-50 p-3 text-red-700">
                    {(error as Error).message || "Failed to load decks."}
                </div>
                <button
                    onClick={() => refetch()}
                    className="mt-3 rounded bg-slate-900 px-3 py-1.5 text-white hover:bg-black"
                >
                    Retry
                </button>
            </div>
        )
    }

    const decks = data ?? []

    return (
        <div className="p-6">
            <div className="mb-4 flex items-center justify-between">
                <h1 className="text-2xl font-bold">My Decks</h1>
                <Link
                    to="/builder"
                    className="rounded bg-indigo-600 px-3 py-1.5 text-white hover:bg-indigo-700"
                >
                    New Deck
                </Link>
            </div>

            {decks.length === 0 ? (
                <div className="rounded border border-slate-200 bg-white p-4 text-slate-600">
                    You don’t have any decks yet. Click <span className="font-medium">New Deck</span> to
                    create one.
                </div>
            ) : (
                <ul className="grid gap-3">
                    {decks.map((deck: Deck) => (
                        <li
                            key={deck.id}
                            className="rounded border border-slate-200 bg-white p-4"
                        >
                            <div className="flex items-start justify-between">
                                <Link
                                    to={`/decks/${deck.id}`}
                                    className="text-lg font-semibold underline"
                                >
                                    {deck.name}
                                </Link>

                                <div className="flex flex-wrap gap-2 min-w-[200px] justify-end">
                                    <span
                                        className={`rounded-full px-2 py-0.5 text-xs ${
                                            deck.is_private
                                                ? "bg-slate-100 text-slate-700"
                                                : "bg-green-100 text-green-700"
                                        }`}
                                    >
                                        {deck.is_private ? "Private" : "Public"}
                                    </span>

                                    {deck.colours?.map((colour: string) => {
                                        const colourMap: Record<string, string> = {
                                            GREEN: "bg-green-200 text-green-800",
                                            RED: "bg-red-200 text-red-800",
                                            BLUE: "bg-blue-200 text-blue-800",
                                            WHITE: "bg-slate-200 text-slate-800",
                                            PURPLE: "bg-purple-200 text-purple-800",
                                        }
                                        return (
                                            <span
                                                key={colour}
                                                className={`rounded-full px-2 py-0.5 text-xs font-medium ${colourMap[colour] || "bg-gray-200 text-gray-800"}`}
                                            >
                                                {colour}
                                            </span>
                                        )
                                    })}

                                    <span className="flex items-center text-sm text-slate-600 ml-auto">
                                        ▲ <span className="ml-1">{deck.vote_count ?? 0}</span>
                                    </span>
                                </div>
                            </div>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    )
}
