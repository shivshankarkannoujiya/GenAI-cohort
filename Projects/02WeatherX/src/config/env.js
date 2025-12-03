import dotenv from "dotenv";

dotenv.config({
    path: "./.env"
})

export const ENV = {
    GEMINI_API_KEY: process.env.GEMINI_API_KEY,
};