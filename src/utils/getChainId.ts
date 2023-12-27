//TODO: Should probably make this dynamic
// const list =  require("./chain_list.json");
import list from "./chain_list.json";
const typedList : any = list;

export function lookUpchain(chainId: string) {
    return typedList[chainId] || chainId;
}

export function lookupScanner(chainId: number) {
    switch(chainId) {
        // Ethereum
        case 1:
            return "https://etherscan.io/address/";
        // Ethereum Goerli
        case 5:
            return "https://goerli.etherscan.io/address/";
        // Optimism
        case 10:
            return "https://optimistic.etherscan.io/address/";
        // Optimism Goerli
        case 420:
            return "https://goerli-optimism.etherscan.io/address/";
        // Public Goods Network
        case 424:
            return "https://explorer.publicgoods.network/address/";
        // Base
        case 8453:
            return "https://basescan.org/address/";
        // Base Goerli
        case 84531:
            return "https://goerli.basescan.org/address/";
        // Ethereum Sepolia
        case 11155111:
            return "https://sepolia.etherscan.io/address/";
        // Optimism Sepolia
        case 11155420:
            return "https://optimism-sepolia.blockscout.com/address/";
        default:
            return "" ;
    }
}
