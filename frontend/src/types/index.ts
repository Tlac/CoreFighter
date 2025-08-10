export type Card = {
    id: string;
    rarity: string;
    name: string;
    level: number | null;
    cost: number | null;
    colour: "GREEN" | "RED" | "BLUE" | "WHITE" | "PURPLE";
    type: string;
    effect: string;
    zone: string[];
    trait: string[];
    link: string;
    ap: string | null;
    hp: string | null;
    title: string;
    set: string;
    image_url: string | null;
    original_image_url: string | null;
    quantity: number;
};

export type Deck = {
    id: string;
    name: string;
    is_private: boolean;
    colours: string[];
    vote_count?: number;
    cards: Card[];
};