import type {Card} from "@/types";

type Props = {
    card: Card;
    width?: number;
    onClick?: () => void;
};


export default function CardTile({card, width = 160, onClick}: Props) {
    return (
        <div
            className="relative overflow-hidden shadow-md transition-transform duration-200 hover:scale-105 hover:shadow-lg"
            style={{width}}
            onClick={onClick}
            title={card.name}
        >
            <img
                src={card.original_image_url ?? "/placeholder-card.png"}
                alt={card.name}
                className="w-full h-auto object-cover"
            />

            <div
                className="absolute top-1 left-1/2 -translate-x-1/2 bg-slate-800 text-white text-sm font-semibold px-4 py-1 rounded-full shadow-md whitespace-nowrap min-w-max">
                {card.id}
            </div>

            <div
                className="absolute bottom-1 left-1/2 -translate-x-1/2 bg-slate-800 text-white text-sm font-semibold px-4 py-1 rounded-full shadow-md whitespace-nowrap min-w-max">
                x{card.quantity}
            </div>
        </div>
    );
}
