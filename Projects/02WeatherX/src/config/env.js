import dotenv from "dotenv";

dotenv.config({
    path: "./.env"
})

export const ENV = {
    OPENAI_API_KEY: process.env.OPENAI_API_KEY,
};