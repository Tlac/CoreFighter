import {useParams, Link} from "react-router-dom";
import {useQuery} from "@tanstack/react-query";

import {api} from "@/api/client";
import {Card, Deck} from "@/types";
import CardTile from "@/components/CardTile";


const colourMap: Record<string, string> = {
    GREEN: "bg-green-200 text-green-800",
    RED: "bg-red-200 text-red-800",
    BLUE: "bg-blue-200 text-blue-800",
    WHITE: "bg-slate-200 text-slate-800",
    PURPLE: "bg-purple-200 text-purple-800",
};

export default function DeckDetail() {
    const {id} = useParams<{ id: string }>();

    const {data, isLoading, isError, error, refetch} = useQuery({
        queryKey: ["deck", id],
        queryFn: () => api<Deck>(`/api/decks/${id}/`),
        enabled: Boolean(id),
    });

    if (isLoading) {
        return (
            <div className="p-6">
                <div className="mb-3">
                    <Link to="/" className="text-indigo-600 underline">← Back</Link>
                </div>
                <p className="text-slate-600">Loading deck…</p>
            </div>
        );
    }

    if (isError) {
        return (
            <div className="p-6">
                <div className="mb-3">
                    <Link to="/" className="text-indigo-600 underline">← Back</Link>
                </div>
                <div className="rounded-md border border-red-200 bg-red-50 p-3 text-red-700">
                    {(error as Error).message || "Failed to load deck."}
                </div>
                <button
                    onClick={() => refetch()}
                    className="mt-3 rounded bg-slate-900 px-3 py-1.5 text-white hover:bg-black"
                >
                    Retry
                </button>
                <p className="mt-2 text-sm text-slate-500">
                    If this is a private deck you don’t own, the server will return an error.
                </p>
            </div>
        );
    }

    const deck = data!;

    return (
        <div className="p-6">
            <div className="mb-3 flex items-center justify-between">
                <Link to="/profile" className="text-indigo-600 underline">← Back</Link>
                <span
                    className={`rounded-full px-2 py-0.5 text-xs ${
                        deck.is_private ? "bg-slate-100 text-slate-700" : "bg-green-100 text-green-700"
                    }`}
                >
                    {deck.is_private ? "Private" : "Public"}
                </span>
            </div>

            <h1 className="text-2xl font-bold">{deck.name}</h1>

            {deck.colours && deck.colours.length > 0 && (
                <div className="mt-3 flex flex-wrap gap-2">
                    {deck.colours.map((card) => (
                        <span
                            key={card}
                            className={`rounded-full px-2 py-0.5 text-xs font-medium ${
                                colourMap[card] || "bg-gray-200 text-gray-800"
                            }`}
                        >
                            {card}
                        </span>
                    ))}
                </div>
            )}

            {"vote_count" in deck && (
                <div className="mt-3 flex items-center text-slate-600">
                    ▲ <span className="ml-1">{deck.vote_count ?? 0}</span>
                </div>
            )}

            {deck.cards && deck.cards.length > 0 && (
                <div className="mt-6">
                    <h2 className="text-lg font-semibold mb-3">Cards</h2>
                    <div
                        className="
                            grid
                            gap-4
                            [grid-template-columns:repeat(auto-fill,minmax(160px,1fr))]
                          "
                    >
                        {deck.cards.map((card: Card) => (
                            <CardTile key={card.id} card={card} width={160}/>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}
